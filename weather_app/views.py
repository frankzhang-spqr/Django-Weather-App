from django.views.generic import View, TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from datetime import datetime
from . import utils
from .models import User
import json

class BaseContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else {}
        context['current_date'] = datetime.now().strftime("%A, %B %d, %Y")
        if self.request.user.is_authenticated:
            # Get weather for favorite cities
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

class RegisterView(BaseContextMixin, View):
    def get(self, request):
        return render(request, 'register.html', self.get_context_data())

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([email, username, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return render(request, 'register.html', self.get_context_data())

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html', self.get_context_data())

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'register.html', self.get_context_data())

        # Check for letters and numbers
        has_letters = any(c.isalpha() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        if not (has_letters and has_numbers):
            messages.error(request, 'Password must contain at least one letter and one number')
            return render(request, 'register.html', self.get_context_data())

        # Check if user exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html', self.get_context_data())

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'register.html', self.get_context_data())

        User.objects.create_user(email=email, username=username, password=password)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

class LoginView(BaseLoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = datetime.now().strftime("%A, %B %d, %Y")
        return context

class WeatherView(BaseContextMixin, View):
    def get(self, request):
        city = request.GET.get('city')
        units = request.GET.get('units', 'imperial')

        if not city:
            messages.error(request, 'Please enter a city name')
            return render(request, 'city-not-found.html', self.get_context_data())

        weather_data = utils.get_current_weather(city.strip(), units)

        if weather_data.get('cod') != 200:
            return render(request, 'city-not-found.html', 
                         self.get_context_data(error=weather_data.get('message', 'City not found')))

        context = self.get_context_data()
        context.update({
            'title': weather_data['name'],
            'status': weather_data['weather'][0]['description'].capitalize(),
            'temp': f"{weather_data['main']['temp']:.1f}",
            'feels_like': f"{weather_data['main']['feels_like']:.1f}",
            'humidity': weather_data['main']['humidity'],
            'wind_speed': f"{weather_data['wind']['speed']:.1f}",
            'icon': weather_data['weather'][0]['icon'],
            'units': "F" if units == "imperial" else "C"
        })
        return render(request, 'weather.html', context)

class LocationWeatherView(BaseContextMixin, View):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        units = request.GET.get('units', 'imperial')

        if not lat or not lon:
            return JsonResponse({"error": "Latitude and longitude are required"}, status=400)

        weather_data = utils.get_location_weather(lat, lon, units)

        if weather_data.get('cod') != 200:
            return render(request, 'city-not-found.html',
                         self.get_context_data(error='Could not get weather for your location'))

        context = self.get_context_data()
        context.update({
            'title': weather_data['name'],
            'status': weather_data['weather'][0]['description'].capitalize(),
            'temp': f"{weather_data['main']['temp']:.1f}",
            'feels_like': f"{weather_data['main']['feels_like']:.1f}",
            'humidity': weather_data['main']['humidity'],
            'wind_speed': f"{weather_data['wind']['speed']:.1f}",
            'icon': weather_data['weather'][0]['icon'],
            'units': "F" if units == "imperial" else "C"
        })
        return render(request, 'weather.html', context)

class ForecastView(BaseContextMixin, View):
    def get(self, request):
        city = request.GET.get('city')
        units = request.GET.get('units', 'imperial')

        if not city:
            messages.error(request, 'Please enter a city name')
            return render(request, 'city-not-found.html', self.get_context_data())

        forecast_data = utils.get_forecast(city.strip(), units)

        if forecast_data.get('cod') != "200":
            return render(request, 'city-not-found.html',
                         self.get_context_data(error=forecast_data.get('message', 'City not found')))

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
        context.update({
            'city': forecast_data['city']['name'],
            'forecasts': list(daily_forecasts.values()),
            'units': "F" if units == "imperial" else "C"
        })
        return render(request, 'forecast.html', context)

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
