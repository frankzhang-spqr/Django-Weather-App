import requests
import os
from typing import Dict, Union, Any
import logging
from django.conf import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from Django settings
API_KEY = settings.WEATHER_API_KEY

if not API_KEY:
    raise EnvironmentError("OpenWeather API key not found. Please set API_KEY in .env file")

BASE_URL = "http://api.openweathermap.org/data/2.5"
GEO_URL = "http://api.openweathermap.org/geo/1.0"

def handle_api_response(response: requests.Response, error_msg: str) -> Dict[str, Any]:
    """Handle API response and errors"""
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"cod": response.status_code, "message": str(http_err)}
    except Exception as err:
        logger.error(f"Error occurred: {err}")
        return {"cod": 500, "message": error_msg}

def get_location_weather(lat: float, lon: float, units: str = "imperial") -> Dict[str, Any]:
    """Get weather data for specific coordinates"""
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": units
        }
        response = requests.get(f"{BASE_URL}/weather", params=params)
        return handle_api_response(response, "Error getting weather data for location")
    except Exception as err:
        logger.error(f"Error getting location weather: {err}")
        return {"cod": 500, "message": "Unable to get weather for location"}

def get_current_weather(city: str, units: str = "imperial") -> Dict[str, Any]:
    """Get current weather data for a city"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }
        response = requests.get(f"{BASE_URL}/weather", params=params)
        return handle_api_response(response, "Error getting current weather data")
    except Exception as err:
        logger.error(f"Error getting current weather: {err}")
        return {"cod": 500, "message": "Unable to get current weather"}

def get_forecast(city: str, units: str = "imperial") -> Dict[str, Any]:
    """Get 5-day weather forecast for a city"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }
        response = requests.get(f"{BASE_URL}/forecast", params=params)
        return handle_api_response(response, "Error getting forecast data")
    except Exception as err:
        logger.error(f"Error getting forecast: {err}")
        return {"cod": "500", "message": "Unable to get forecast data"}

def get_city_by_coords(lat: float, lon: float) -> Dict[str, Any]:
    """Get city name from coordinates using reverse geocoding"""
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "limit": 1,
            "appid": API_KEY
        }
        response = requests.get(f"{GEO_URL}/reverse", params=params)
        data = handle_api_response(response, "Error getting location data")
        
        if isinstance(data, list) and len(data) > 0:
            return {"cod": 200, "name": data[0].get("name", "Unknown Location")}
        return {"cod": 404, "message": "Location not found"}
    except Exception as err:
        logger.error(f"Error getting city by coords: {err}")
        return {"cod": 500, "message": "Unable to get location information"}

def search_cities(query: str) -> list:
    """Search for cities using geocoding API"""
    try:
        params = {
            "q": query,
            "limit": 5,
            "appid": API_KEY
        }
        response = requests.get(f"{GEO_URL}/direct", params=params)
        data = handle_api_response(response, "Error searching cities")
        
        if isinstance(data, list):
            return [{"name": city.get("name", ""),
                    "state": city.get("state", ""),
                    "country": city.get("country", "")} 
                    for city in data]
        return []
    except Exception as err:
        logger.error(f"Error searching cities: {err}")
        return []
