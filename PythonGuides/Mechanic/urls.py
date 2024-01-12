from django.urls import path
from .views import *

urlpatterns = [
    path('signup_mech',signup_mech,name='signup_mech'),
    path('mech_details',mech_details,name='mech_details'),
    path('mech_login',mech_login,name='mech_login'),
    path('update_map',update_map,name='update_map'),
    path('get_card_data',get_card_data,name='get_card_data'),
]

