import os
import requests
import json
import logging
from difflib import get_close_matches

logger = logging.getLogger(__name__)

def get_current_weather(city, units='imperial'):
    """Get current weather for a city."""
    try:
        api_key = os.getenv('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': api_key,
            'units': units
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX and 5XX status codes
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        return {'cod': response.status_code, 'message': str(http_err)}
    except Exception as err:
        logger.error(f'Error occurred: {err}')
        return {'cod': 500, 'message': str(err)}

def get_location_weather(lat, lon, units='imperial'):
    """Get weather for specific coordinates."""
    try:
        api_key = os.getenv('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': units
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        return {'cod': response.status_code, 'message': str(http_err)}
    except Exception as err:
        logger.error(f'Error occurred: {err}')
        return {'cod': 500, 'message': str(err)}

def get_forecast(city, units='imperial'):
    """Get 5-day forecast for a city."""
    try:
        api_key = os.getenv('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': city,
            'appid': api_key,
            'units': units
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        return {'cod': response.status_code, 'message': str(http_err)}
    except Exception as err:
        logger.error(f'Error occurred: {err}')
        return {'cod': '500', 'message': str(err)}

def get_city_suggestions(city):
    """Get similar city name suggestions."""
    common_cities = [
        'London', 'New York', 'Tokyo', 'Paris', 'Sydney', 'Singapore', 'Dubai',
        'Berlin', 'Madrid', 'Rome', 'Moscow', 'Beijing', 'Mumbai', 'Seoul',
        'Toronto', 'Los Angeles', 'Chicago', 'Miami', 'Vancouver', 'Melbourne',
        'Amsterdam', 'Barcelona', 'Vienna', 'San Francisco', 'Seattle',
        'Hong Kong', 'Bangkok', 'Istanbul', 'Rio de Janeiro', 'Mexico City'
    ]
    
    # Get close matches from common cities
    matches = get_close_matches(city, common_cities, n=5, cutoff=0.6)
    
    # If no matches found, try searching with OpenWeather API
    if not matches:
        try:
            api_key = os.getenv('API_KEY')
            url = 'http://api.openweathermap.org/geo/1.0/direct'
            params = {
                'q': city,
                'limit': 5,
                'appid': api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract city names from API response
            api_suggestions = [f"{item['name']}, {item.get('country', '')}" for item in data]
            matches.extend(api_suggestions)
            
        except Exception as err:
            logger.error(f'Error getting city suggestions: {err}')
    
    return list(dict.fromkeys(matches))  # Remove duplicates while preserving order

def sanitize_city_name(city):
    """Clean and validate city name."""
    if not city:
        return ''
    
    # Remove special characters and extra spaces
    clean_city = ''.join(c for c in city if c.isalnum() or c.isspace() or c == '-')
    clean_city = ' '.join(clean_city.split())
    
    return clean_city

def format_temperature(temp, units='imperial'):
    """Format temperature with proper unit symbol."""
    try:
        temp = float(temp)
        unit_symbol = '°F' if units == 'imperial' else '°C'
        return f"{temp:.1f}{unit_symbol}"
    except (ValueError, TypeError):
        return 'N/A'
