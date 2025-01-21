import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_current_weather(city="Kansas City", units="imperial"):
    try:
        request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units={units}'
        response = requests.get(request_url)
        response.raise_for_status()  # Check if the request was successful
        weather_data = response.json()
        return weather_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"cod": "404", "message": "City not found"}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"cod": "500", "message": "An error occurred with the weather service."}

def get_forecast(city="Kansas City", units="imperial"):
    try:
        request_url = f'http://api.openweathermap.org/data/2.5/forecast?appid={os.getenv("API_KEY")}&q={city}&units={units}'
        response = requests.get(request_url)
        response.raise_for_status()  # Check if the request was successful
        forecast_data = response.json()
        return forecast_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"cod": "404", "message": "City not found"}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"cod": "500", "message": "An error occurred with the weather service."}