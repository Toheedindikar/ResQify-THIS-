from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .encrypt_util import *
from .forms import *
from home.models import * 
import googlemaps
# Create your views here.
def signup_mech(request):
    if request.method == 'POST':
        if  request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password1 = request.POST['pass1']
            password2 = request.POST['pass2']
            print(name)
            if (password1 == password2):
                encryptpass= encrypt(password1)
                if UsersMechanic.objects.filter(username =username).exists():
                    
                    return HttpResponse('User already exits')
                else:
                    data = UsersMechanic(name=name,username=username,email=email,mobile=phone,password= encryptpass)
                    data.save()
                    form = mech_detailsModelForm()
                    return redirect('mech_details')
                
            else:
                return render(request, 'login_final.html')
        
    return render(request,'Mechanic/login_final.html')

def mech_details(request):
    if request.method == 'POST':
        form = mech_detailsModelForm(request.POST)
        mech_address = request.POST.get('mech_Address')
        mech_city = request.POST.get('mech_city')
        mech_zipcode = request.POST.get('mech_zipcode')
        mech_shop = request.POST.get('mech_shop')

        if form.is_valid():
            form.save()
        locations=[]
        key = settings.GOOGLE_API_KEY
        udata = UsersCurrentAddress.objects.all()
        adress_string = str(mech_shop)+", "+str(mech_address)+", "+str(mech_zipcode)+", "+str(mech_city)+", "+"India"

        gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
        result = gmaps.geocode(adress_string)[0]    
        lat = result.get('geometry', {}).get('location', {}).get('lat', None)
        lng = result.get('geometry', {}).get('location', {}).get('lng', None)
        data = {
                    "lat":float(lat), 
                    "lng": float(lng), 
                    "color":'red',  
                }
        locations.append(data)
        for i in udata:  
            print(i.lat)
            data = {
                    "lat":float(i.lat), 
                    "lng": float(i.lng), 
                    "color":'blue',  
                }

            locations.append(data)

            print(locations)
        context = {
            "key": key, 
           "locations": locations,
            'form': form
             
            } 
        return render(request,'Mechanic/mechdashboard.html',context=context)
         
    else:
        form = mech_detailsModelForm()

    return render(request,'Mechanic/mech_details.html',{'form': form})