from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .encrypt_util import *
from .forms import *
from home.models import * 
import googlemaps
import json
from datetime import datetime

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
                    profile = Profile(mech_username=username,mech_name = name)
                    profile.no_of_bookings = 0
                    profile.save()
                    return redirect('mech_details')
                
            else:
                return render(request, 'login_final.html')
        
    return render(request,'Mechanic/login_final.html')

def mech_details(request):
    if request.method == 'POST':
       
        username = request.session['username']
        
            # Accessing form values
        mech_shop = request.POST['mech_shop']
        mech_address = request.POST['address']
        mech_zipcode = request.POST['mech_zipcode']
        mech_city = request.POST['mech_city']
        print("inside",mech_shop)
        adress_string = str(mech_shop)+", "+str(mech_address)+", "+str(mech_zipcode)+", "+str(mech_city)+", "+"India"
        gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
        result = gmaps.geocode(adress_string)[0]    
        lat = result.get('geometry', {}).get('location', {}).get('lat', None)
        lng = result.get('geometry', {}).get('location', {}).get('lng', None)
        data = MechanicDetails(mech_shop=mech_shop,mech_Address= mech_address,mech_zipcode=mech_zipcode,mech_city=mech_city,username=username,lat = lat,lng = lng)
        data.save()
      
        
        return redirect('mech_login')
         
   

    return render(request,'Mechanic/mech_details.html')

def mech_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        try:
            verify = UsersMechanic.objects.get(username = username)
            password = request.POST['password']
            
            decrypted = decrypt(verify.password)
            if(decrypted == password):
                request.session['name'] = verify.name
                request.session['username'] = verify.username
                return redirect('mech_dashboard')
            else:
                return HttpResponse('user not found or the password is wrong')
           
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


def get_vehicle_data(request):
    username = request.session['username']
    mech_address = MechanicDetails.objects.get(username = username)

    from_adress_string = str(mech_address.mech_shop)+", "+str(mech_address.mech_Address)+", "+str(mech_address.mech_city)+", "+str(mech_address.mech_zipcode)
    user_address = UsersCurrentAddress.objects.all()
    now = datetime.now()
    data = []
    i =0 
    for address in user_address:
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        result = gmaps.reverse_geocode((address.lat, address.lng))
        add = result[0]['formatted_address']
        # update = UsersCurrentAddress(username = username,lat = address.lat,lng =address.lng,address = add)
        # update.save()
        gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
        calculate = gmaps.distance_matrix(
                    from_adress_string,
                    add,
                    mode = 'driving',
                    departure_time = now
            )
        duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
        duration_minutes = duration_seconds/60

        distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
        distance_kilometers = distance_meters/1000
        
        var = {
                'username': address.username,
                'issue_description': 'the vehicle is not starting',
                'contact': '2343143',
                'distance': distance_kilometers,
                'time':duration_minutes
            }
        data.append(var)
        print(var)
        i += 1 
        if (i == 5):
            exit
    print(data)
        

    return JsonResponse(data, safe=False)
@csrf_exempt
def next_page(request):
    # Assuming you want to pass the selected card data to the next page
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process data as needed
        
        print('Received data:', data)
        for i in data:
            print(i)

    # Your other view logic goes here

    return HttpResponse("Response from Django backend")

def mech_dashboard(request):
            username = request.session['username']
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

def display_info(request,username):
    cust_username = username
    key = settings.GOOGLE_API_KEY
    mech_username = request.session['username']
    mech_address = MechanicDetails.objects.get(username = mech_username)

    from_adress_string = str(mech_address.mech_shop)+", "+str(mech_address.mech_Address)+", "+str(mech_address.mech_city)+", "+str(mech_address.mech_zipcode)
    add = UsersCurrentAddress.objects.get(username = cust_username)
    username = UsersCustomer.objects.get(username = cust_username)
    mech_name = UsersMechanic.objects.get(username = mech_username )
    to_address = add.address
    cust_lat = add.lat
    print(cust_lat)
    cust_lng = add.lng
    mech_lat = mech_address.lat
    mech_lng = mech_address.lng
    print(mech_lat,mech_lng)
    now = datetime.now()
    gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
    calculate = gmaps.distance_matrix(
                    from_adress_string,
                    to_address,
                    mode = 'driving',
                    departure_time = now
    )
    locations = []
    data = {
        'cust_lat':float(cust_lat),
        'cust_lng':float(cust_lng),
        'mech_lat':float(mech_lat),
        'mech_lng':float(mech_lng)
    }
    print(cust_lat)
    locations.append(data)
    duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
    duration_minutes = duration_seconds
    # duration_seconds = duration_seconds*60
    distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
    distance_kilometers = distance_meters/1000
    # status = Booking_status(issueid = add.issueid , cust_name = username.name ,cust_username = cust_username,mech_name = mech_name.name,mech_username = request.session['username'], mech_assigned = 1,issue_resolved_status = 0,cust_lat = cust_lat,cust_lng = cust_lng,mech_lat = mech_lat,mech_lng=mech_lng  )
    # status.save()
    current_datetime = datetime.now()
    def month_name(month_number):
        month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        return month_names[month_number - 1]

    # Format the datetime
    formatted_datetime = current_datetime.strftime("%d %B %Y ")
    time = current_datetime.strftime("%H:%M:%S")
    
    # Replace the month number with the month name
    formatted_datetime = formatted_datetime.replace(
        current_datetime.strftime("%B"), month_name(current_datetime.month)
    )
    status = Booking_status.objects.get(cust_username = cust_username )
    status.issueid = add.issueid
    status.cust_name = username.name
    status.mech_name = mech_name.name
    status.mech_username = request.session['username']
    status.mech_assigned = 1
    status.issue_resolved_status = 0
    status.cust_lat = cust_lat
    status.cust_lng = cust_lng
    status.mech_lat = mech_lat
    status.mech_lng = mech_lng
    status.duration_kilometers = distance_kilometers
    status.duration_seconds = duration_seconds
    status.booking_time = time
    status.booking_date = formatted_datetime
    status.save()
    profile = Profile.objects.get(mech_username = mech_username )
    val = int(profile.no_of_bookings)
    val +=1
    profile.save()
    
    return render(request,'Mechanic/display_test.html',
                  {'card_data':cust_username,
                   'cust_name':username.name ,
                   'key':key,'duration_minutes':duration_minutes,
                   'distance_kilometers':distance_kilometers,
                   'locations' :locations,
                   'phone' : add.phone,
                   'address': add.address,
                   'duration_seconds':duration_seconds,
                   })
    # return render(request,"Mechanic/resolved_page.html")
    # return HttpResponse("hekk",vehicle_number)
def logout_mech(request):
    if 'username' in request.session:
        del request.session['username']
        
    if 'name' in request.session:
        del request.session['name']
    
    # You can perform additional logout actions here if needed

    return redirect('home_page')

def home_page(request):
    return render(request,"Home_Page.html")

def mech_profile(request):
    data = UsersMechanic.objects.get(username = request.session['username'] )
    mech_name = data.name

    profile = Profile.objects.get(mech_username = request.session['username'] )
    no_of_bookings = profile.no_of_bookings
    rating = profile.rating
    phone = UsersMechanic.objects.get(username = request.session['username'] )
    mobile = phone.mobile
    return render(request,"Mechanic/profile.html",{'mech_name':mech_name,'no_of_bookings':no_of_bookings,'rating':rating,'phone':mobile})

def mech_feedback(request):
    if request.method == 'POST':
        resolved =  request.POST['Resolved']
        print(resolved)
        unresolved = request.POST['Unresolved']
        status = Booking_status.objects.get(mech_username = request.session['username'] )
        if resolved:
            status.issue_resolved_status = 1
        else:
            status.issue_resolved_status = 0
        status.save()
        return redirect('home_page')


    return render(request,"Mechanic/feedback.html")

def mech_resolved(request):
    if request.method == 'POST':
        status = Booking_status.objects.get(mech_username = request.session['username'] )
        status.issue_resolved_status = 1
        status.save()
    return  redirect('home_page')

def mech_unresolved(request):
    if request.method == 'POST':
        status = Booking_status.objects.get(mech_username = request.session['username'] )
        status.issue_resolved_status = 0
        status.save()
    return  redirect('home_page')

def mech_bookings(request):
    return render(request,"Mechanic/Bookings.html")