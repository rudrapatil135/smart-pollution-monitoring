from django.db import models

# Create your models here.
from django.db import models

class PollutantReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    no2 = models.FloatField()
    so2 = models.FloatField()
    co = models.FloatField()
    o3 = models.FloatField()
    
    class Meta:
        ordering = ['timestamp']
