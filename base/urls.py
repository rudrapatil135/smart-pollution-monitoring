from django.urls import path
from . import views
urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_view,name='logout'),
]