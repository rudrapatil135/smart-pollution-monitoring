from django.urls import path
from .views import station_aqi, pollution_page

urlpatterns = [
    path('aqi/stations/', station_aqi, name='station_aqi'),
    path('pollution/', pollution_page, name='pollution'),
]
