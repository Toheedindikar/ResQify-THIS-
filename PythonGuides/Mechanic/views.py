from django.shortcuts import render,HttpResponse
from .models import *
from .encrypt_util import *
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
                    return render(request,'Mechanic/login_final.html')
                
            else:
                return render(request, 'login_final.html')
        
    return render(request,'Mechanic/login_final.html')
