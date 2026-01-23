from django.urls import path 
from .views import source_attribution
urlpatterns = [
    path('source_attribution/',source_attribution,name='source_attribution'),
]