# Weather Forecast Web Application (Django + Open-Meteo API)



Веб-приложение, позволяющее пользователю ввести название города и получить прогноз погоды на ближайшие часы.
Проект реализован с использованием Django , использует Open-Meteo API для получения данных о погоде, хранит историю посещений городов и поддерживает работу через Docker.

---



## Основные функции


- Ввод названия города и получение прогноза погоды
- Отображение погоды в удобочитаемом формате
- Сохранение последнего просмотренного города в куках
- История поиска городов
- REST API для просмотра статистики поиска городов
- Тестирование pytest
- Контейнеризация с помощью Docker
- 
Приложение написано на Python с использованием Django.

---

## Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Dimon4ik812/weather_forecast
cd weather-forecast
```

### 2. Создайте .env файл
```
SECRET_KEY=your-secret-key-here
DEBUG=True

POSTGRES_DB=weather_db
POSTGRES_USER=weather_user
POSTGRES_PASSWORD=weather_password
```

### 3. Убедитесь, что установлены
```
• Docker
• Docker Compose
```

## Запуск
```commandline
1. docker-compose up -d --build
2. docker-compose exec web python manage.py migrate
3. Откройте браузер и перейдите по адресу: http://0.0.0.0:8000/
```

## Использование
```commandline
 • Python — основной язык программирования.
 • Django — веб-фреймворк для создания приложения.
 • Open-Meteo API — прогноз погоды
 • Nominatim (OpenStreetMap) — Геокодер для получения координат
 • PostgreSQL — хранение истории посещений
 • Requests - Для работы с внешними API
 • Pytest - Тестирование
 
 
```