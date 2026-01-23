
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('api/',include('pollution.urls')),
    path('pollution/',include('pollution.urls')),
    path('policy/',include('policy.urls')),
]
