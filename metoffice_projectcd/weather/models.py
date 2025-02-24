from django.db import models

class WeatherData(models.Model):
    location_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    temperature = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.region}"
