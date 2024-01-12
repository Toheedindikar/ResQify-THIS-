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
            request.session['username'] = username
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
        form.username = request.session['username']
        if form.is_valid():
            form.save()
        
        return redirect('mech_login')
         
    else:
        form = mech_detailsModelForm()

    return render(request,'Mechanic/mech_details.html',{'form': form})

def mech_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        try:
            verify = UsersMechanic.objects.get(username = username)
            password = request.POST['password']
            print(verify.username)
            decrypted = decrypt(verify.password)
            if(decrypted == password):
                request.session['name'] = verify.name
                request.session['username'] = verify.username
                print(decrypted)
            locations=[]
            key = settings.GOOGLE_API_KEY
            print(key)
            mech_addr = MechanicDetails.objects.get(username = username)
            print(mech_addr)
            udata = UsersCurrentAddress.objects.all()
            print("break")
            adress_string = str(mech_addr.mech_shop)+", "+str(mech_addr.mech_Address)+", "+str(mech_addr.mech_zipcode)+", "+str(mech_addr.mech_city)+", "+"India"
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
                
                
                } 
            return render(request,'Mechanic/mechdashboard.html',context=context)
        except Exception as e:
            print(f"Exception: {e}")
            return HttpResponse("An error occurred during login.")
    
    return render(request,'Mechanic/login_final.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def update_map(request):
    locations=[]
    key = settings.GOOGLE_API_KEY
    print(key)
    mech_addr = MechanicDetails.objects.get(username = request.session['username'])
    print(mech_addr)
    udata = UsersCurrentAddress.objects.all()
    print("break")
    adress_string = str(mech_addr.mech_shop)+", "+str(mech_addr.mech_Address)+", "+str(mech_addr.mech_zipcode)+", "+str(mech_addr.mech_city)+", "+"India"
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
            
    # context = {
    #     "key": key, 
    #     "locations": locations,
    #             } 
    return JsonResponse(locations, safe=False)

@csrf_exempt
def get_card_data(request):
    data = []
    card_data = {
        'title': 'Dynamic Title',
        'description': 'Dynamic Vehicle Description',
    }
    data.append(card_data)
    return JsonResponse(card_data, safe=False)
