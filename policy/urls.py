from django.urls import path 
from .views import ai_policy_decision, aqi_forecast, last_hour_pollutants, live_pollutants, policy_dashboard, policy_simulation, source_attribution, historical_trends, historical_trends_data, station_details, aqi_forecast, satellite_data
urlpatterns = [
    path('source_attribution/',source_attribution,name='source_attribution'),
    path('policy_simulation/', policy_simulation, name='policy_simulation'),
    path("ai-policy-decision/", ai_policy_decision, name="ai_policy_decision"),
    path("policy_dashboard/", policy_dashboard, name="policy_dashboard"),
    path('live_pollutants/', live_pollutants, name='live_pollutants'),
    path('last_hour_pollutants/', last_hour_pollutants, name='last_hour_pollutants'),
    path("historical-trends/", historical_trends, name="historical_trends"),
    path("historical-trends_data/", historical_trends_data, name="historical_trends_data"),
    path("station-details/", station_details, name="station_details"),
    path("aqi-forecast/", aqi_forecast, name="aqi_forecast"),
    path("satellite-data/", satellite_data, name="satellite_data"),

]

