from django.urls import path
from .views import *

urlpatterns = [
    path('', navbar, name='navbar'),
    path('signup',signup,name='signup'),
    path('login',login,name='login'),
    path('location',save_location,name='save_location'),
    path('BookMechanic',BookMechanic,name='BookMechanic'),
]