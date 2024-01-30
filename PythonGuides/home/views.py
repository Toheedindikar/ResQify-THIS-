from django.shortcuts import render,redirect
from django.http import HttpResponse
from requests import session
from. models import *
from Mechanic.models import *
from home.encrypt_util import *
import googlemaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.core.mail import send_mail
from PythonGuides.settings import EMAIL_HOST_USER

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
            # zipcode = result[0]['postal_code']
            udata.address= address
            # udata.zipcode = zipcode
            udata.save()
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

    return render(request, 'loading_bar.html')




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
                issue = Booking_status(cust_username=username)
                issue.save()
                profil = Profile(cust_username=username,rating = 5,phone=phone,no_of_bookings = 0,cust_name = name)
                profil.save()
                request.session['username'] = username
                return redirect('otp')
        else:
            return render(request, 'login_final.html')
  
    return render(request, 'login_final.html')


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        p1 = request.POST.get('p1', '')
        p2 = request.POST.get('p2', '')
        if(p1 == p2):
            request.session['username'] = username
            request.session['newp'] = p1
            return redirect ('otp_forgot_passwd')
    return render(request, 'forgot_password.html')  


global num
num = 0
def otp_forgot_passwd(request):
    global num
    if request.method == 'POST':
        otp = request.POST.get('otp', '')
        if (int(otp) == int(num)):
            dat = UsersCustomer.objects.get(username = request.session['username'])
            encryptpass= encrypt(request.session['newp'])
            dat.password = encryptpass
            dat.save()
            messages.success(request, 'OTP verified successfully!')
            return redirect('login')
        else:
            messages.success(request, 'OTP not verified successfully!')
            return HttpResponse('invalid Otp')
    else:
        mail = UsersCustomer.objects.get(username = request.session['username'])
        num = random.randrange(1000,9999)
        send_mail('your otp is','your otp is {}'.format(num),EMAIL_HOST_USER,[mail.email],fail_silently=True)
        return  render(request,"forgot_password_otp.html")
            


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
                return redirect('accept_rules')
        except:
            return HttpResponse("Either the user does not exists or the password is wrong")

        # if (verify == username):
        #     print(username)
        return HttpResponse("done")

    return render(request,'login_final.html')

def logout_cust(request):
    if 'username' in request.session:
        del request.session['username']
        
    if 'name' in request.session:
        del request.session['name']
    
    # You can perform additional logout actions here if needed

    return redirect('home_page')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # This is used to exempt the view from CSRF protection. Use it cautiously.
def save_location(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            lat = request.COOKIES.get("lat")
            long = request.COOKIES.get("long")
            print(latitude)
            print(longitude)
            print("post req ")
            username = (request.session['username'])
            print("save location call")
            # idata = UsersCurrentAddress(username=username,lat = latitude,lng = longitude)
            # idata.save()
            udata = UsersCurrentAddress.objects.get(username = username)
            udata.lat = latitude
            udata.lng = longitude
            udata.save()
            # if (UsersCustomer.objects.filter(username =username).exists() == True):
      
    
            key = settings.GOOGLE_API_KEY
            # eligable_locations = Locations.objects.filter(place_id__isnull=False)
            locations = []
            print("Called from login")
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
        username = request.session['username']
        Address = request.POST['Address']
        City = request.POST['City']
        ZipCode = request.POST['ZipCode']
        print(Address)
        adress_string = str(Address)+", "+str(ZipCode)+", "+str(City)+", "+"India"

        gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
        result = gmaps.geocode(adress_string)[0]    
        lat = result.get('geometry', {}).get('location', {}).get('lat', None)
        lng = result.get('geometry', {}).get('location', {}).get('lng', None)
        print(lat)
        print(lng)
        udata = UsersCurrentAddress.objects.get(username = username)
        udata.lat = lat
        udata.lng = lng

        return render(request,"issue_detailpage.html") 
        # Address = request.POST['Address']
        # City = request.POST['City']
        # ZipCode = request.POST['ZipCode']
        # print(Address)
        # adress_string = str(Address)+", "+str(ZipCode)+", "+str(City)+", "+"India"

        # gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
        # result = gmaps.geocode(adress_string)[0]    
        # lat = result.get('geometry', {}).get('location', {}).get('lat', None)
        # lng = result.get('geometry', {}).get('location', {}).get('lng', None)
        # # print(lat)
        # # print(lng)F
        # # return HttpResponse("success")
        # gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        # result = gmaps.reverse_geocode((lat, lng))

        # if result:
        #         # Assuming the first result is the most relevant one
        #     address = result[0]['formatted_address']

        #     print(f"Address: {address}")
        #     return HttpResponse(address)
        # else:
        #     print("Reverse geocoding API did not return any results.")
        #     return HttpResponse("No address found")

def loc(request):
    return render(request,"index.html") 

import random

# Generate a random integer between a specified range

def vehicle_details(request):
    if request.method == 'POST':
        username = request.session['username']
        print(username)
        vehicleType = request.POST['vehicleType']
        vehicleNumber = request.POST['vehicleNumber']
        issueDescription = request.POST['issueDescription']
        print(vehicleType)
        mobileNumber = request.POST['mobileNumber']
        issueId = random.randint(1, 1000)
        undata = UsersCurrentAddress.objects.get(username = username)
        status = Booking_status.objects.get(cust_username= username)
        status.issue_resolved_status = 0
        status.mech_assigned = 0
        try :
            update = BookMechanic.objects.get(username = username)
            update.issueid = issueId
            update.Address = undata.address
            update.ZipCode = 560060
            update.vehicleNo = vehicleNumber
            update.phone = mobileNumber
            update.save()
        except:
            # udata = UsersCurrentAddress(issueid = '2',Address = undata.address,ZipCode = 560060 ,VehicleType = vehicleType,VehicleNo = vehicleNumber,Issuedesc = issueDescription,Phone = mobileNumber)
            undata.issueid = issueId
            undata.phone = mobileNumber
            undata.issuedesc = issueDescription
            undata.vehicleNo = vehicleNumber
            undata.vehicleType = vehicleType
            print("except called")
            undata.save()
        username = (request.session['username'])
        print(username)
            # idata = UsersCurrentAddress(username=username,lat = latitude,lng = longitude)
            # idata.save()
        udata = UsersCurrentAddress.objects.get(username = username)
        latitude = udata.lat
        longitude = udata.lng
        udata.save()
            # if (UsersCustomer.objects.filter(username =username).exists() == True):
      
    
        key = settings.GOOGLE_API_KEY
            # eligable_locations = Locations.objects.filter(place_id__isnull=False)
        locations = []
        print("Called from login")
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
            
        return render(request, 'loading_bar.html', context)

        

    return render(request,"issue_detailpage.html") 
    
def accept_rules(request):
    return render(request,"accept_rules.html") 


def check_mechanic(request):
    cust_username = request.session['username']
    status = Booking_status.objects.get(cust_username = cust_username )
    print(cust_username)
    booked = status.mech_assigned
    print(booked)
    
    if booked == '1':
        
        data = {'status': 'found'}
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'not_found'})
    return JsonResponse(data)
    

def mech_booked(request):
    return render(request,"accept_rules.html") 

def profile(request):
    profile = Profile.objects.get(cust_username =request.session['username'] )
    
    return render(request,"profile.html",{'phone' : profile.phone, 'rating' : profile.rating,'no_of_bookings':profile.no_of_bookings,'cust_name':profile.cust_name})


def waiting_page(request):
    cust_username = request.session['username']
    status = Booking_status.objects.get(cust_username = cust_username )
    mech_username = status.mech_username
    mech_name = status.mech_name
    cust_lat = status.cust_lat
    cust_lng = status.cust_lng
    mech_lat = status.mech_lat
    mech_lng = status.mech_lng
    duration_seconds = status.duration_seconds
    key = settings.GOOGLE_API_KEY
    duration_kilometers = status.duration_kilometers
    mech = UsersMechanic.objects.get(username= mech_username)
    mech_add = MechanicDetails.objects.get(username = mech_username)
    locations = []
    data = {
        'cust_lat':float(cust_lat),
        'cust_lng':float(cust_lng),
        'mech_lat':float(mech_lat),
        'mech_lng':float(mech_lng)
    }
    print(cust_lat)
    locations.append(data)
    return render(request,'waiting_page.html',
                  {'card_data':mech_username,
                   'cust_name':mech_name,
                   'key':key,'duration_minutes':duration_seconds,
                   'distance_kilometers':duration_kilometers,
                   'locations' :locations,
                   'phone' : mech.mobile,
                   'address': mech_add.mech_Address,
                   'duration_seconds':duration_seconds,
                   })

from .forms import FeedbackForm
def feedback(request):
    if request.method == 'POST':
        cust_username = request.session['username']
        status = Booking_status.objects.get(cust_username = cust_username )
        feedback_desc = request.POST.get('desc', '')
        
        # try:
        #     star1 = request.POST["star1"]
        #     rating = 1
        # except:
        #     star2 = request.POST["star2"]
        #     rating = 2
        rating = 4
        
        feed = Feedback(issueid = status.issueid,desc = feedback_desc,rating = rating,cust_name= status.cust_name,cust_username= status.cust_username,mech_name = status.mech_name ,mech_username= status.mech_username)
        feed.save()
        status.issue_resolved_status = 1
        status.mech_assigned = 0
        status.save()
        booking = Bookings(booking_time = status.booking_time,booking_date= status.booking_date,mech_name = status.mech_name ,cust_username =cust_username)
        mech_phone = UsersMechanic.objects.get(username = status.mech_username)
        booking.phone = mech_phone.mobile
        issue = UsersCurrentAddress.objects.get(username = cust_username)
        booking.issue_desc = issue.issuedesc
        booking.save()   
        profile = Profile.objects.get(mech_username = status.mech_username )
        profile.rating = 4

        profile.save()

        return redirect('home_page')
    else:
        form = FeedbackForm()
    return render(request,"feedback.html", {'form': form})

def home_page(request):
    return render(request,"Home_Page.html") 

def Booking_histroy(request):
    cust_username = request.session['username']
    bookings = []
    book_data = Bookings.objects.filter(cust_username = cust_username)
    for i in book_data:
        
        data = {
            "booking_time" : i.booking_time,
            "booking_date" : i.booking_date,
            "mech_name" : i.mech_name,
            
            "issue_desc" : i.issue_desc 
        }
        bookings.append(data)

    return render(request,"Bookings.html",{"bookings":bookings})

from django.contrib import messages
global no
no = 0
def otp(request):
    global no
    if request.method == 'POST':
        otp = request.POST.get('otp', '')
        if (int(otp) == int(no)):
            messages.success(request, 'OTP verified successfully!')
            return redirect('login')
        else:
            messages.success(request, 'OTP verified successfully!')
            return HttpResponse('invalid')
    else:
        mail = UsersCustomer.objects.get(username = request.session['username'])
        no = random.randrange(1000,9999)
        send_mail('your otp is','your otp is {}'.format(no),EMAIL_HOST_USER,[mail.email],fail_silently=True)
        return  render(request,"otp.html")