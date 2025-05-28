
from weather_forecast.models import CitySearchHistory

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .services import get_weather, update_city_history, get_coordinates
import logging
from urllib.parse import quote
from urllib.parse import unquote

logger = logging.getLogger(__name__)

class IndexView(View):
    template_name = 'weather_forecast/index.html'

    def get(self, request, *args, **kwargs):
        city = request.GET.get('city', '').strip()

        weather_data = None

        if city:
            try:
                # Получаем координаты города
                latitude, longitude = get_coordinates(city)
                if not latitude or not longitude:
                    weather_data = {"error": "Город не найден"}
                else:
                    # Получаем прогноз по координатам
                    weather_data = get_weather(latitude, longitude, city=city)
                    # Обновляем историю поиска
                    update_city_history(request.user, city)
            except Exception as e:
                logger.error(f"Ошибка при получении данных для города '{city}': {e}", exc_info=True)
                weather_data = {"error": "Не удалось получить данные о погоде"}

        last_city = request.COOKIES.get('last_city', '')

        context = {
            'weather': weather_data,
            'last_city': last_city
        }

        response = render(request, self.template_name, context)

        if city and weather_data and "error" not in weather_data:
            response.set_cookie('last_city', quote(city), max_age=60 * 60 * 24 * 7)  # кодируем куку

        return response



class CityAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        cities = CitySearchHistory.objects.filter(city_name__icontains=query) \
                     .values_list('city_name', flat=True).distinct()[:10]
        return JsonResponse(list(cities), safe=False)



class CityStatsApiView(View):
    def get(self, request, *args, **kwargs):
        stats = CitySearchHistory.objects.all().order_by('-search_count')[:10]
        result = {item.city_name: item.search_count for item in stats}
        return JsonResponse(result)



class HistoryView(View):
    template_name = 'weather_forecast/history.html'

    def get(self, request, *args, **kwargs):
        history = CitySearchHistory.objects.all().order_by('-last_searched')
        decoded_history = [
            {
                "city_name": unquote(item.city_name),
                "search_count": item.search_count,
                "last_searched": item.last_searched
            }
            for item in history
        ]
        return render(request, self.template_name, {'history': decoded_history})