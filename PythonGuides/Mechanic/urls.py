from django.urls import path
from .views import *

urlpatterns = [
    path('signup_mech',signup_mech,name='signup_mech'),
    path('mech_details',mech_details,name='mech_details'),
    path('mech_login',mech_login,name='mech_login'),
    path('update_map',update_map,name='update_map'),
    path('get_card_data',get_card_data,name='get_card_data'),
    path('get_vehicle_data',get_vehicle_data,name='get_vehicle_data'),
    path('mechanic/next_page',next_page,name='next_page'),
    path('mech_dashboard',mech_dashboard,name='mech_dashboard'),
    path('display_info/<str:vehicle_number>/',display_info,name='display_info'),
    path('process_request',process_request,name='process_request'),
]

