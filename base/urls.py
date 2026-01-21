from django.urls import path
from . import views
urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
]