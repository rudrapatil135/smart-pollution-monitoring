from django.urls import path
from .views import map_view, station_aqi, pollution_page, forecast_api

from pollution import views

urlpatterns = [
    path('aqi/stations/', station_aqi, name='station_aqi'),
    path('pollution/', pollution_page, name='pollution'),
    path('pollution/map/',map_view,name='map'),
    path("forecast/", views.forecast_api, name="forecast_api"),
    path('routes/',views.routes,name='routes'),
    path('alerts/',views.alerts,name='alerts'),
    path('satellite/',views.satellite,name='satellite'),
]
