from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
from weather import get_current_weather, get_forecast, get_location_weather, get_city_by_coords
from waitress import serve
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import init_db, User, db
from werkzeug.security import check_password_hash
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Initialize database
db = init_db(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def format_date():
    return datetime.now().strftime("%A, %B %d, %Y")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate input
        if not all([email, username, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html', current_date=format_date())

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html', current_date=format_date())

        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html', current_date=format_date())

        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html', current_date=format_date())
            
        # Simple check for letters and numbers
        has_letters = any(c.isalpha() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        if not (has_letters and has_numbers):
            flash('Password must contain at least one letter and one number', 'error')
            return render_template('register.html', current_date=format_date())

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html', current_date=format_date())

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return render_template('register.html', current_date=format_date())

        # Create new user
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', current_date=format_date())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html', current_date=format_date())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', current_date=format_date())

@app.route('/get_location_weather')
def get_location_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'imperial')
    
    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400
        
    api_key = os.environ.get('API_KEY')
    try:
        # First get weather data directly using coordinates
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={api_key}"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        if weather_data.get('cod') == 200:
            return render_template(
                "weather.html",
                title=weather_data["name"],
                status=weather_data["weather"][0]["description"].capitalize(),
                temp=f"{weather_data['main']['temp']:.1f}",
                feels_like=f"{weather_data['main']['feels_like']:.1f}",
                humidity=weather_data['main']['humidity'],
                wind_speed=f"{weather_data['wind']['speed']:.1f}",
                icon=weather_data['weather'][0]['icon'],
                units="F" if units == "imperial" else "C",
                current_date=format_date(),
                user=current_user
            )
        else:
            return render_template('city-not-found.html', 
                                error="Could not get weather for your location",
                                current_date=format_date())
    except Exception as e:
        return render_template('city-not-found.html', 
                             error="Error getting weather data",
                             current_date=format_date())

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    units = request.args.get('units', 'imperial')

    if not city:
        return render_template('city-not-found.html', 
                             error="Please enter a city name",
                             current_date=format_date())

    weather_data = get_current_weather(city.strip(), units)

    if weather_data.get('cod') != 200:
        return render_template('city-not-found.html', 
                             error=weather_data.get('message', 'City not found'),
                             current_date=format_date())

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        humidity=weather_data['main']['humidity'],
        wind_speed=f"{weather_data['wind']['speed']:.1f}",
        icon=weather_data['weather'][0]['icon'],
        units="F" if units == "imperial" else "C",
        current_date=format_date(),
        user=current_user
    )

@app.route('/forecast')
def forecast():
    city = request.args.get('city')
    units = request.args.get('units', 'imperial')

    if not city:
        return render_template('city-not-found.html', 
                             error="Please enter a city name",
                             current_date=format_date())

    forecast_data = get_forecast(city.strip(), units)

    if forecast_data.get('cod') != "200":
        return render_template('city-not-found.html', 
                             error=forecast_data.get('message', 'City not found'),
                             current_date=format_date())

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

    return render_template(
        "forecast.html",
        city=forecast_data['city']['name'],
        forecasts=list(daily_forecasts.values()),
        units="F" if units == "imperial" else "C",
        current_date=format_date(),
        user=current_user
    )

@app.route('/toggle_favorite', methods=['POST'])
@login_required
def toggle_favorite():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    if city in current_user.favorite_cities:
        current_user.remove_favorite_city(city)
        return jsonify({'status': 'removed'})
    else:
        current_user.add_favorite_city(city)
        return jsonify({'status': 'added'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        serve(app, host="0.0.0.0", port=port)
