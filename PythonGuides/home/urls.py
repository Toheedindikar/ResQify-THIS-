from django.urls import path
from .views import *

urlpatterns = [
    path('navbar', navbar, name='navbar'),
    path('signup',signup,name='signup'),
    path('login',login,name='login'),
    path('save_location',save_location,name='save_location'),
    path('BookMechanic',BookMechanic,name='BookMechanic'),
    path('loc',loc,name="loc"), 
    path('vehicle_details',vehicle_details,name="vehicle_details"), 
    path('accept_rules',accept_rules,name="accept_rules")
]