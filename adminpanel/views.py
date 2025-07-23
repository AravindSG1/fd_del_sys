from django.shortcuts import render, redirect
from restaurants.models import Restaurant
from django.http import HttpResponse
from accounts.models import LoginTable
from orders.models import Order
from payments.models import Payment
from accounts.forms import LoginTableForm
from restaurants.forms import RestaurantForm
from customers.forms import CustomerProfileForm
from delivery.models import DeliveryAgentProfile
from delivery.forms import DeliveryAgentProfileForm

# Create your views here.
def admin_dashboard(request):
    all_users = LoginTable.objects.all().count()
    total_admins = LoginTable.objects.filter(is_superuser=1).count()
    total_users = all_users - total_admins

    total_restaurants = Restaurant.objects.all().count()
    total_orders = Order.objects.all().count()
    total_agents = LoginTable.objects.filter(is_delivery=1).count()
    payment_objs = Payment.objects.all()
    total_money = 0
    for payment in payment_objs:
        total_money+= payment.amount
    return render(request, 'adminpanel/admin_dashboard.html', 
                  {'total_users':total_users, 'total_restaurants':total_restaurants, 
                   'total_orders':total_orders, 'total_agents':total_agents,
                   "total_money":total_money})

#------------------------------------------Customers----------------------------------------------------
def admin_manage_users(request):
    user_obj = LoginTable.objects.filter(is_customer=1)
    return render(request, 'adminpanel/admin_manage_users.html', {'users':user_obj})

def delete_customer(request, id):
    customer_obj = LoginTable.objects.get(id=id)
    customer_obj.delete()
    return redirect(admin_manage_users)

def customer_details(request, id):
    user_obj = LoginTable.objects.get(id=id)    
    return render(request, 'adminpanel/customer_details.html', {'user':user_obj})

def customer_edit(request, id):   
    user_obj = LoginTable.objects.get(id=id) 
    customer_obj = user_obj.customerprofile
    form_obj_user = LoginTableForm(instance=user_obj)
    form_obj_customer = CustomerProfileForm(instance=customer_obj)
    if request.method == 'GET':
        return render(request, 'adminpanel/customer_edit.html', 
                    {'form_user':form_obj_user, 'form_customer':form_obj_customer})
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST, instance=user_obj)
        form_obj_customer = CustomerProfileForm(request.POST, request.FILES, instance=customer_obj)
        
        if form_obj_user.is_valid() and form_obj_customer.is_valid():
            form_obj_user.save()
            form_obj_customer.save()
            return redirect(admin_manage_users)  # Redirect to the same profile page after saving

    return render(request, 'adminpanel/customer_details.html', {
        'form_user': form_obj_user,
        'form_res': form_obj_customer,        
    })
#----------------------------------------------Restaurants-----------------------------------------------------
def admin_restaurants(request):
    approved_restaurants = Restaurant.objects.filter(is_approved=1)
    on_hold_res = Restaurant.objects.filter(is_approved=0)
    return render(request, 'adminpanel/admin_restaurants.html',
                  {'approved_restaurants':approved_restaurants, 'on_hold_res':on_hold_res})

def restaurant_approval(request, id):
    res_obj = Restaurant.objects.get(id=id)
    res_obj.is_approved = True
    res_obj.save()    
    return redirect(admin_restaurants)

def restaurant_details(request, id):
    restaurant_obj = Restaurant.objects.get(id=id)
    user_obj = restaurant_obj.owner
    form_obj_user = LoginTableForm(instance=user_obj)
    form_obj_restaurant = RestaurantForm(instance=restaurant_obj)
    return render(request, 'adminpanel/restaurant_details.html', 
                  {'user':user_obj, 'form_user':form_obj_user, 'form_res':form_obj_restaurant})

def restaurant_edit(request, id):
    user_obj = LoginTable.objects.get(id=id)
    restaurant_obj = user_obj.restaurant
    form_obj_user = LoginTableForm(instance=user_obj)
    form_obj_restaurant = RestaurantForm(instance=restaurant_obj)
    if request.method == 'GET':        
        return render(request, 'adminpanel/restaurant_edit.html', 
                    {'user':user_obj, 'form_user':form_obj_user, 'form_res':form_obj_restaurant})
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST, instance=user_obj)
        form_obj_restaurant = RestaurantForm(request.POST, request.FILES, instance=user_obj.restaurant)
        
        if form_obj_user.is_valid() and form_obj_restaurant.is_valid():
            form_obj_user.save()
            form_obj_restaurant.save()
            return redirect(admin_restaurants)  # Redirect to the same profile page after saving

    return render(request, 'adminpanel/admin_restaurants.html', {
        'form_user': form_obj_user,
        'form_res': form_obj_restaurant,
        'user': user_obj
    })

def delete_restaurant(request, id):
    restaurant_obj = Restaurant.objects.get(id=id)
    restaurant_obj.delete()
    return redirect(admin_restaurants)

#-----------------------------------------------Orders------------------------------------------------
def admin_orders(request):
    order_objs = Order.objects.all()
    return render(request, 'adminpanel/admin_orders.html', {'orders':order_objs})

#-------------------------------------------Payments----------------------------------------------------
def admin_payments(request):
    payment_obj = Payment.objects.all()
    return render(request, 'adminpanel/admin_payments.html', {'payments':payment_obj})

#------------------------------------------Delivery Agents---------------------------------------------------
def admin_delivery_agents(request):
    delivery_agent_obj = DeliveryAgentProfile.objects.all()
    return render(request, 'adminpanel/admin_delivery_agents.html', {'agents':delivery_agent_obj})

def delete_delivery_agents(request, id):
    delivery_agents_obj = DeliveryAgentProfile.objects.get(id=id)
    delivery_agents_obj.delete()
    return redirect(admin_delivery_agents)

def delivery_agent_details(request, id):
    agent_obj = DeliveryAgentProfile.objects.get(id=id)
    return render(request, 'adminpanel/delivery_agent_details.html', {'agent':agent_obj})

def delivery_agent_edit(request, id):  
    delivery_agent_obj = DeliveryAgentProfile.objects.get(id=id)  
    user_obj = delivery_agent_obj.agent
    form_obj_user = LoginTableForm(instance=user_obj)
    form_obj_delivery = DeliveryAgentProfileForm(instance=delivery_agent_obj)
    if request.method == 'GET':
        return render(request, 'adminpanel/delivery_agent_edit.html', 
                    {'form_user':form_obj_user, 'form_delivery':form_obj_delivery})
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST, instance=user_obj)
        form_obj_delivery = DeliveryAgentProfileForm(request.POST, request.FILES, instance=delivery_agent_obj)
        
        if form_obj_user.is_valid() and form_obj_delivery.is_valid():
            form_obj_user.save()
            form_obj_delivery.save()
            return redirect(admin_delivery_agents)  # Redirect to the same profile page after saving

    return render(request, 'adminpanel/delivery_agent_details.html', {
        'form_user': form_obj_user,
        'form_delivery': form_obj_delivery,        
    })

