from django.views.generic import View, TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.urls import reverse_lazy
from datetime import datetime
from django.db import transaction
from . import utils
from .models import User
import json
import logging

logger = logging.getLogger(__name__)

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else {}
        context['current_date'] = datetime.now().strftime("%A, %B %d, %Y")
        if self.request.user.is_authenticated:
            favorite_weather = []
            for city in self.request.user.favorite_cities:
                weather = utils.get_current_weather(city)
                if weather.get('cod') == 200:
                    favorite_weather.append({
                        'city': city,
                        'temp': f"{weather['main']['temp']:.1f}",
                        'status': weather['weather'][0]['description'].capitalize(),
                        'icon': weather['weather'][0]['icon']
                    })
            context['favorite_weather'] = favorite_weather
        return context

class IndexView(BaseContextMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_center'] = json.dumps([0, 20])
        context['map_zoom'] = 2
        return context

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = datetime.now().strftime("%A, %B %d, %Y")
        return context

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get('username', '').strip().lower()  # Form uses 'username' field for email
            password = request.POST.get('password', '')
            
            logger.info(f"Login attempt for email: {email}")
            
            if not email or not password:
                messages.error(request, 'Please enter both email and password')
                return self.form_invalid(None)
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                logger.info(f"User {user.username} logged in successfully")
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password')
                logger.warning(f"Login failed for email: {email}")
                return self.form_invalid(None)

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred during login. Please try again.')
            return self.form_invalid(None)

    def form_invalid(self, form):
        return render(self.request, self.template_name, self.get_context_data())

class RegisterView(BaseContextMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'register.html', self.get_context_data())

    def post(self, request):
        try:
            email = request.POST.get('email', '').strip().lower()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            context = self.get_context_data()

            # Validation checks
            if not all([email, username, password, confirm_password]):
                messages.error(request, 'All fields are required')
                return render(request, 'register.html', context)

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'register.html', context)

            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
                return render(request, 'register.html', context)

            has_letters = any(c.isalpha() for c in password)
            has_numbers = any(c.isdigit() for c in password)
            if not (has_letters and has_numbers):
                messages.error(request, 'Password must contain at least one letter and one number')
                return render(request, 'register.html', context)

            # Check if email is valid
            if '@' not in email:
                messages.error(request, 'Please enter a valid email address')
                return render(request, 'register.html', context)

            # Check username length and characters
            if len(username) < 3:
                messages.error(request, 'Username must be at least 3 characters long')
                return render(request, 'register.html', context)

            # Check if user exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return render(request, 'register.html', context)

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return render(request, 'register.html', context)

            # Create user in a transaction
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password
                )
                user.favorite_cities = []
                user.save()

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'register.html', self.get_context_data())

class CustomLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'Successfully logged out.')
        return redirect('index')

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'Successfully logged out.')
        return redirect('index')

class WeatherView(BaseContextMixin, View):
    def get(self, request):
        city = request.GET.get('city', '').strip()
        units = request.GET.get('units', 'imperial')

        if not city:
            return render(request, 'index.html', self.get_context_data())

        try:
            # Clean city name
            city = utils.sanitize_city_name(city)
            weather_data = utils.get_current_weather(city, units)

            if weather_data.get('cod') != 200:
                # Get city suggestions
                suggestions = utils.get_city_suggestions(city)
                context = self.get_context_data()
                context.update({
                    'error': weather_data.get('message', 'City not found'),
                    'suggestions': suggestions,
                    'units': "F" if units == "imperial" else "C"
                })
                return render(request, 'city-not-found.html', context)

            context = self.get_context_data()
            # Format coordinates for JavaScript
            lon = float(weather_data['coord']['lon'])
            lat = float(weather_data['coord']['lat'])
            
            context.update({
                'title': weather_data['name'],
                'status': weather_data['weather'][0]['description'].capitalize(),
                'temp': utils.format_temperature(weather_data['main']['temp'], units),
                'feels_like': utils.format_temperature(weather_data['main']['feels_like'], units),
                'humidity': weather_data['main']['humidity'],
                'wind_speed': f"{weather_data['wind']['speed']:.1f}",
                'icon': weather_data['weather'][0]['icon'],
                'units': "F" if units == "imperial" else "C",
                'map_center': json.dumps([lon, lat]),
                'map_zoom': 10
            })
            return render(request, 'weather.html', context)
        except Exception as e:
            logger.error(f"Weather error: {str(e)}")
            messages.error(request, 'Error getting weather data. Please try again.')
            context = self.get_context_data()
            context.update({
                'error': 'Error getting weather data. Please try again.',
                'suggestions': utils.get_city_suggestions(city),
                'units': "F" if units == "imperial" else "C"
            })
            return render(request, 'city-not-found.html', context)

class LocationWeatherView(BaseContextMixin, View):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        units = request.GET.get('units', 'imperial')

        if not lat or not lon:
            messages.error(request, 'Location data is required')
            return render(request, 'index.html', self.get_context_data())

        try:
            weather_data = utils.get_location_weather(lat, lon, units)

            if weather_data.get('cod') != 200:
                messages.error(request, 'Could not get weather for your location')
                return render(request, 'city-not-found.html',
                            self.get_context_data(error='Could not get weather for your location'))

            context = self.get_context_data()
            context.update({
                'title': weather_data['name'],
                'status': weather_data['weather'][0]['description'].capitalize(),
                'temp': utils.format_temperature(weather_data['main']['temp'], units),
                'feels_like': utils.format_temperature(weather_data['main']['feels_like'], units),
                'humidity': weather_data['main']['humidity'],
                'wind_speed': f"{weather_data['wind']['speed']:.1f}",
                'icon': weather_data['weather'][0]['icon'],
                'units': "F" if units == "imperial" else "C",
                'map_center': json.dumps([float(lon), float(lat)]),
                'map_zoom': 10
            })
            return render(request, 'weather.html', context)
        except Exception as e:
            logger.error(f"Location weather error: {str(e)}")
            messages.error(request, 'Error getting weather data. Please try again.')
            return render(request, 'city-not-found.html',
                        self.get_context_data(error='Error getting weather data. Please try again.'))

class ForecastView(BaseContextMixin, View):
    def get(self, request):
        city = request.GET.get('city', '').strip()
        units = request.GET.get('units', 'imperial')

        if not city:
            messages.error(request, 'Please enter a city name')
            return render(request, 'index.html', self.get_context_data())

        try:
            # Clean city name
            city = utils.sanitize_city_name(city)
            forecast_data = utils.get_forecast(city, units)

            if forecast_data.get('cod') != "200":
                # Get city suggestions
                suggestions = utils.get_city_suggestions(city)
                context = self.get_context_data()
                context.update({
                    'error': forecast_data.get('message', 'City not found'),
                    'suggestions': suggestions,
                    'units': "F" if units == "imperial" else "C"
                })
                return render(request, 'city-not-found.html', context)

            # Group forecast data by day
            daily_forecasts = {}
            for item in forecast_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'date': datetime.fromtimestamp(item['dt']).strftime('%A, %B %d'),
                        'temp_min': float('inf'),
                        'temp_max': float('-inf'),
                        'icon': item['weather'][0]['icon'],
                        'description': item['weather'][0]['description'].capitalize(),
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    }
                
                daily_forecasts[date]['temp_min'] = min(daily_forecasts[date]['temp_min'], item['main']['temp_min'])
                daily_forecasts[date]['temp_max'] = max(daily_forecasts[date]['temp_max'], item['main']['temp_max'])

            context = self.get_context_data()
            # Format coordinates for JavaScript
            lon = float(forecast_data['city']['coord']['lon'])
            lat = float(forecast_data['city']['coord']['lat'])
            
            context.update({
                'city': forecast_data['city']['name'],
                'forecasts': list(daily_forecasts.values()),
                'units': "F" if units == "imperial" else "C",
                'map_center': json.dumps([lon, lat]),
                'map_zoom': 10
            })
            return render(request, 'forecast.html', context)
        except Exception as e:
            logger.error(f"Forecast error: {str(e)}")
            messages.error(request, 'Error getting forecast data. Please try again.')
            context = self.get_context_data()
            context.update({
                'error': 'Error getting forecast data. Please try again.',
                'suggestions': utils.get_city_suggestions(city),
                'units': "F" if units == "imperial" else "C"
            })
            return render(request, 'city-not-found.html', context)

class ToggleFavoriteView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            data = json.loads(request.body)
            city = data.get('city')
            
            if not city:
                return JsonResponse({'error': 'City name is required'}, status=400)

            if city in request.user.favorite_cities:
                request.user.remove_favorite_city(city)
                return JsonResponse({'status': 'removed'})
            else:
                request.user.add_favorite_city(city)
                return JsonResponse({'status': 'added'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
