from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from customers.views import customer_homepage
from restaurants.views import restaurant_dashboard
from delivery.views import delivery_agent_dashboard
from adminpanel.views import admin_dashboard
from django.contrib import messages
# Create your views here.

def login_page(request):
    if request.method == "GET":
        return render(request, 'core/login.html')
    elif request.method == "POST":        
        username = request.POST["username"]        
        password = request.POST['password'] 
        
        user = authenticate(request, username=username, password=password)
        #user is an instance of custom user model
        
        if user is not None:
            login(request, user)
            if user.is_superuser:                
                return redirect(admin_dashboard)
            if user.is_customer:
                return redirect(customer_homepage)
            elif user.is_restaurant:
                return redirect(restaurant_dashboard)
            elif user.is_delivery:
                return redirect(delivery_agent_dashboard)     
        else:
            messages.error(request, "Wrong login credentials")
            return redirect(login_page)    
    else:
        return render(request, 'core/login.html')       
    
def user_logout(request):
    logout(request)          #this line is must to end session otherwise, function just renders loginpage
    return redirect(login_page)

    

    
