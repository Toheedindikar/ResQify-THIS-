from django.urls import path
from .views import *

urlpatterns = [
    path('signup_mech',signup_mech,name='signup_mech'),
]

