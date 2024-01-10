from django.urls import path
from .views import *

urlpatterns = [
    path('signup_mech',signup_mech,name='signup_mech'),
    path('mech_details',mech_details,name='mech_details'),
]

