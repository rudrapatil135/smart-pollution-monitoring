from django.db import models

# Create your models here.

class PollutantReading(models.Model):
    timestamp = models.DateTimeField()
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    no2 = models.FloatField()
    so2 = models.FloatField()
    co = models.FloatField()
    o3 = models.FloatField()
    
    class Meta:
        ordering = ['timestamp']

class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Delhi")
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
