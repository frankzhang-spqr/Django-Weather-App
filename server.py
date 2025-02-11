from flask import Flask, render_template, request, jsonify
from weather import get_current_weather, get_forecast
from waitress import serve
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def format_date():
    return datetime.now().strftime("%A, %B %d, %Y")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', current_date=format_date())

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
        current_date=format_date()
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
        current_date=format_date()
    )

@app.route('/search')
def search_cities():
    """Endpoint for city search suggestions"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    # This would ideally use a geocoding API
    # For now, return a simple response
    return jsonify([{"name": query}])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        serve(app, host="0.0.0.0", port=port)
