from django.conf import settings

def weather_settings(request):
    return {
        'WEATHER_API_KEY': settings.WEATHER_API_KEY,
    }
