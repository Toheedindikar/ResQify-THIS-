from django.shortcuts import render
from django.http import HttpResponse
from requests import session
from. models import *
from home.encrypt_util import *
import googlemaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def navbar(request):
    if request.method == 'POST':
        username = (request.session['username'])
        print(username)
        # udata = UsersCurrentAddress.objects.get(username = username)
        key = settings.GOOGLE_API_KEY
            # eligable_locations = Locations.objects.filter(place_id__isnull=False)
        if UsersCustomer.objects.filter(username =username).exists():
            udata = UsersCurrentAddress.objects.get(username = username)
            locations = []
            latitude = udata.lat
            longitude = udata.lng
            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            result = gmaps.reverse_geocode((latitude, longitude))
            address = result[0]['formatted_address']
            print(result)
        for a in range(0,1): 
            data = {
                    "lat":float(latitude), 
                    "lng": float(longitude), 
                    "name":'',  
                }

            locations.append(data)

            print(locations)
        context = {
            "key": key, 
           "locations": locations,
            "address" : address,
             
            }
            
        return render(request, 'customer_map.html', context=context)

    return render(request, 'navbar.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        print('Original Password:', request.POST['password'])
        encryptpass= encrypt(request.POST['password'])
        print('Encrypt Password:',encryptpass)
        decryptpass= decrypt(encryptpass)
        print('Decrypt Password:',decryptpass)
        data=EmpLogin(name=name, email=email, password=password)
        data = UsersCustomer(name=name)
        data.save()
        return HttpResponse('Done')
    else:
        return render(request, 'login_final.html')


def signup(request):
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
            if UsersCustomer.objects.filter(username =username).exists():
                
                return HttpResponse('User already exits')
            else:
                data = UsersCustomer(name=name,username=username,email=email,mobile=phone,password= encryptpass)
                data.save()
                ldata = UsersCurrentAddress(username=username)
                ldata.save()
                return render(request, 'login_final.html')
            
        else:
            return render(request, 'login_final.html')
  
    return render(request, 'login_final.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username'] 
        try:
            verify = UsersCustomer.objects.get(username = username)
            password = request.POST['password']
            print(verify.username)
            decrypted = decrypt(verify.password)
            if(decrypted == password):
                request.session['name'] = verify.name
                request.session['username'] = verify.username
                return loc(request)
        except:
            return HttpResponse("Either the user does not exists or the password is wrong")

        # if (verify == username):
        #     print(username)
        return HttpResponse("done")

    return render(request,'login_final.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # This is used to exempt the view from CSRF protection. Use it cautiously.
def save_location(request):
    # variable = request.COOKIES.get("lat")
    # long = request.COOKIES.get("long")
    # print(variable)
    # print(long)
    if request.method == 'POST':
        try:
            # data = request.POST  # Use request.POST to access form data
            # latitude = data.get('lat')
            # longitude = data.get('long')
            # print(latitude)
            # print(longitude)
            # You can now do something with the latitude and longitude, such as saving it to the database
            # Example: Save to a model
            # location = UserLocation(latitude=latitude, longitude=longitude)
            # location.save()
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            lat = request.COOKIES.get("lat")
            long = request.COOKIES.get("long")
            print(latitude)
            print(longitude)
            print("post req ")
            username = (request.session['username'])
            print(username)
            # idata = UsersCurrentAddress(username=username,lat = latitude,lng = longitude)
            # idata.save()
            udata = UsersCurrentAddress.objects.get(username = username)
            udata.lat = latitude
            udata.lng = longitude
            udata.save()
            # if (UsersCustomer.objects.filter(username =username).exists() == True):
            #     udata = UsersCurrentAddress.objects.get(username = username)
            #     udata.lat = latitude
            #     udata.lng = longitude
            # else:
            #     print("else called")
            #     data = UsersCurrentAddress(username=username,lat = latitude,lng = longitude)
            #     data.save()

    
            key = settings.GOOGLE_API_KEY
            # eligable_locations = Locations.objects.filter(place_id__isnull=False)
            locations = []

            for a in range(0,1): 
                data = {
                    "lat":float(latitude), 
                    "lng": float(longitude), 
                    "name":'',
                    
                }

                locations.append(data)

            print(locations)
            context = {
                "key": key, 
                "locations": locations
            }
            
            return render(request, 'customer_map.html', context)


            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request,"location.html")


def BookMechanic(request):
    if request.method == 'POST':
        Address = request.POST['Address']
        City = request.POST['City']
        ZipCode = request.POST['ZipCode']
        print(Address)
        adress_string = str(Address)+", "+str(ZipCode)+", "+str(City)+", "+"India"

        gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
        result = gmaps.geocode(adress_string)[0]    
        lat = result.get('geometry', {}).get('location', {}).get('lat', None)
        lng = result.get('geometry', {}).get('location', {}).get('lng', None)
        # print(lat)
        # print(lng)
        # return HttpResponse("success")
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        result = gmaps.reverse_geocode((lat, lng))

        if result:
                # Assuming the first result is the most relevant one
            address = result[0]['formatted_address']
            print(f"Address: {address}")
            return HttpResponse(address)
        else:
            print("Reverse geocoding API did not return any results.")
            return HttpResponse("No address found")

def loc(request):
    return render(request,"location.html") 

    
    
