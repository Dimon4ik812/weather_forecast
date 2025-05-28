import requests
from .models import CitySearchHistory
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)

def get_coordinates(city):
    """Получает координаты города через Nominatim API"""
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "WeatherApp/1.0"
    }
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None, None
    except (requests.RequestException, IndexError, ValueError) as e:
        print(f"Ошибка получения координат: {e}")
        return None, None


def get_weather(latitude, longitude, city=None):
    """Получает прогноз погоды по координатам"""
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation_probability,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "city": city or f"{latitude}, {longitude}",
            "current_temp": data["hourly"]["temperature_2m"][0],
            "unit": data["hourly_units"]["temperature_2m"],
            "precipitation": data["hourly"]["precipitation_probability"][0],
            "wind_speed": data["hourly"]["wind_speed_10m"][0],
            "time": data["hourly"]["time"][0]
        }
    except (requests.RequestException, KeyError, IndexError) as e:
        raise Exception(f"Ошибка при получении погоды: {e}")

def update_city_history(user, city_name):
    if not city_name:
        return
    obj, created = CitySearchHistory.objects.get_or_create(
        city_name__iexact=city_name,
        defaults={"city_name": city_name}
    )
    if not created:
        obj.search_count += 1
        obj.last_searched = timezone.now()
        obj.save()