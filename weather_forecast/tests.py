from django.test import TestCase, override_settings
from django.urls import reverse
from .models import CitySearchHistory
from django.contrib.auth.models import User
import tempfile
import os


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class IndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_index_page_loads_successfully(self):
        """Проверяет, что URL / доступен и рендерится корректно."""
        response = self.client.get(reverse('weather_forecast:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather_forecast/index.html')

    def test_weather_search_for_valid_city(self):
        """Проверяет, что функциональность получения прогноза работает для реального города"""
        response = self.client.get(f'{reverse('weather_forecast:index')}?city=Moscow')
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.context)
        self.assertNotIn('error', response.context['weather'])

    def test_weather_search_for_invalid_city(self):
        """Проверяет, что приложение не падает с ошибкой , если пользователь ввёл неверный город."""
        response = self.client.get(f'{reverse('weather_forecast:index')}?city=InvalidCityNameXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.context)
        self.assertIn('error', response.context['weather'])

    def test_cookie_sets_last_city(self):
        """Убеждается, что сайт запоминает последний введённый город."""
        response = self.client.get(f'{reverse('weather_forecast:index')}?city=Moscow')
        self.assertTrue('last_city' in response.cookies)
        last_city_cookie = response.cookies['last_city'].value
        self.assertEqual(last_city_cookie, 'Moscow')

    def test_history_updates_on_city_search(self):
        """Проверяет, что логика хранения истории посещений работает правильно."""
        self.client.get(f'{reverse('weather_forecast:index')}?city=Moscow')
        city_obj = CitySearchHistory.objects.filter(city_name__iexact='Moscow').first()
        self.assertIsNotNone(city_obj)
        self.assertGreaterEqual(city_obj.search_count, 1)

    def test_does_not_create_empty_search(self):
        """Убеждается, что история посещений не засоряется пустыми запросами."""
        self.client.get(reverse('weather_forecast:index'))
        self.assertEqual(CitySearchHistory.objects.count(), 0)