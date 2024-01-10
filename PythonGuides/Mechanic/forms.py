from django import forms
from .models import *

class mech_detailsModelForm(forms.ModelForm):
    class Meta:
        model = MechanicDetails
        fields = ['mech_Address', 'mech_city', 'mech_zipcode', 'mech_shop', 'username', 'lat', 'lng']
