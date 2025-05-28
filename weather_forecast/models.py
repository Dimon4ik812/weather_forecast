from django.db import models
from django.contrib.auth.models import User

class CitySearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100)
    search_count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city_name} ({self.search_count})"
