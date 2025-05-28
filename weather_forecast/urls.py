from django.urls import path
from .views import IndexView, CityAutocompleteView, CityStatsApiView, HistoryView
from weather_forecast.apps import WeatherForecastConfig


app_name = WeatherForecastConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('city-autocomplete/', CityAutocompleteView.as_view(), name='city-autocomplete'),
    path('api/city-stats/', CityStatsApiView.as_view(), name='city-stats-api'),
    path('history/', HistoryView.as_view(), name='history'),
]

