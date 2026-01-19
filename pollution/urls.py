from django.urls import include, path
from . import views
urlpatterns = [
    path('aqi/',views.aqi_api, name='aqi_api'),
    path('',views.dashboard, name='pollution'),
    path('',include('base.urls')),
]
