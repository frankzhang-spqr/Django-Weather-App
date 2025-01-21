# Updated Code with All Features Except Favorite Locations

from flask import Flask, render_template, request
from weather import get_current_weather, get_forecast
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    units = request.args.get('units', 'imperial')

    if not city.strip():
        city = "Kansas City"

    weather_data = get_current_weather(city, units)

    if weather_data.get('cod') != 200:
        return render_template('city-not-found.html', error=weather_data.get('message', 'City not found'))

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        icon=weather_data['weather'][0]['icon'],
        units=units
    )

@app.route('/forecast')
def forecast():
    city = request.args.get('city')
    units = request.args.get('units', 'imperial')

    if not city.strip():
        city = "Kansas City"

    forecast_data = get_forecast(city, units)

    if forecast_data.get('cod') != "200":
        return render_template('city-not-found.html', error=forecast_data.get('message', 'City not found'))

    return render_template("forecast.html", forecast=forecast_data)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)