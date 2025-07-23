from django.shortcuts import render,redirect
from accounts.forms import *
from .forms import *
from core.views import homepage
from django.http import HttpResponse
from orders.models import Order
from django.contrib.auth.decorators import login_required #for login to work on all pages
from django.contrib.auth import login

# Create your views here.
#--------------------------------------Registration Form-----------------------------------------------------
def restaurant_form(request):
    if request.method == 'GET':
        form_obj_user = LoginTableForm()
        form_obj_restaurant = RestaurantForm()
        return render(request,'restaurants/restaurant_form.html', {'user':form_obj_user, 'restaurant':form_obj_restaurant})
    
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST)
        form_obj_restaurant = RestaurantForm(request.POST, request.FILES) 
            
        if form_obj_user.is_valid() and form_obj_restaurant.is_valid():            
            #save the logintable
            form_obj_user = form_obj_user.save(commit = False)
            form_obj_user.is_restaurant = True   #assigning role
            form_obj_user.set_password(form_obj_user.password)  #hashing password
            form_obj_user.save()

            #save restaurant profile 
            form_obj_restaurant = form_obj_restaurant.save(commit= False)
            form_obj_restaurant.is_approved = False   #Admin has to give approval
            form_obj_restaurant.owner = form_obj_user   #link to logintable instance
            form_obj_restaurant.save()
            login(request, form_obj_user)
        return redirect(restaurant_dashboard)
    
    else:        
        return redirect(restaurant_form)

#-------------------------------------------dashboard--------------------------------------------------------
from django.utils.timezone import now
def restaurant_dashboard(request):
    if request.user.restaurant.is_approved:
        today = now().date()  # Get today's date (timezone-aware)        
        order_objs = request.user.restaurant.orders.filter(placed_at__date=today)
        total_order_nos = order_objs.count()        
        preparing = order_objs.filter(status='preparing').count()        
        delivered = order_objs.filter(status='delivered').count()        
        cancelled = order_objs.filter(status='cancelled').count()
        total = 0
        for order in order_objs:
            total += order.total_amount

        return render(request, 'restaurants/restaurant_dashboard.html', 
                      {'total_order_nos':total_order_nos, 'preparing':preparing,
                       'delivered':delivered, 'cancelled':cancelled, 'total':total})   

    else:
        from accounts.views import login_page
        from django.contrib import messages
        messages.error(request, "Your account is not approved yet.")
        return redirect(login_page)
    

#---------------------------------------Food Items--------------------------------------------------
def restaurant_fooditems(request):
    restaurant_obj = request.user.restaurant
    # restaurant_obj = Restaurant.objects.get(id=id)
    food_items_obj = restaurant_obj.food_items.all()  #gives queryset of all food items
    return render(request, 'restaurants/restaurant_fooditems.html', {'fooditems':food_items_obj})        

def food_item(request):            #Adds new food item
    if request.method == 'GET':
        form_obj = FoodItemForm()
        print(request.user) 
        return render(request, 'restaurants/add_food.html',{'food':form_obj})
    elif request.method == 'POST':
        form_obj = FoodItemForm(request.POST, request.FILES)
        if form_obj.is_valid():
            food_obj = form_obj.save(commit=False)
            food_obj.restaurant = request.user.restaurant
            food_obj.save()
            return redirect(restaurant_fooditems)
        else:
            form_obj = FoodItemForm()
            return render(request, 'restaurants/add_food.html',{'food':form_obj})
    else:
        form_obj = FoodItemForm()
        return render(request, 'restaurants/add_food.html',{'food':form_obj})
    
def delete_food(request, id):
    food_obj = FoodItem.objects.get(id=id)
    food_obj.delete()
    return redirect(restaurant_fooditems)

def edit_food(request, id):
    food_obj = FoodItem.objects.get(id=id)
    if request.method == 'GET':
        form_obj = FoodItemForm(instance=food_obj)
        return render(request, 'restaurants/add_food.html', {'food':form_obj})
    elif request.method == 'POST':
        form_obj = FoodItemForm(request.POST, request.FILES, instance=food_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(restaurant_fooditems)
    else:
        return redirect(restaurant_fooditems)
    
#-----------------------------------------Orders--------------------------------------------------------
def restaurant_orders(request):
    active_orders_obj = request.user.restaurant.orders.filter(      #this is a relatedManager obj to filtered query set
        status__in=['pending', 'preparing', 'ready','out_of_delivery'],
        payment__status = 'success').order_by('-placed_at')        # filters only if related Payment has status 'success'
    completed_orders_obj = request.user.restaurant.orders.filter(
        status__in=['delivered','cancelled']).order_by('-updated_at')
    
    if request.method == 'GET':                
        return render(request, 'restaurants/restaurant_orders.html', 
                      {'active_orders':active_orders_obj,
                       'completed_orders':completed_orders_obj})
    elif request.method == 'POST':
        order_id = request.POST['order_id']
        new_status = request.POST.get('status')
        print(order_id, 'this is order id')

        order_obj = Order.objects.get(id=order_id)
        order_obj.status = new_status
        order_obj.save()
        return redirect(restaurant_orders)
    
#--------------------------------------------Profile--------------------------------------------------
@login_required(login_url='login_page')
def restaurant_profile(request):
    user_obj = request.user
    form_obj_user = LoginTableForm(instance=request.user)
    form_obj_restaurant = RestaurantForm(instance=request.user.restaurant)
    return render(request, 'restaurants/restaurant_profile.html', 
                  {'user':user_obj, 'form_user':form_obj_user, 'form_res':form_obj_restaurant})

@login_required(login_url='login_page')
def restaurant_edit_profile(request):
    user_obj = request.user
    restaurant_obj = request.user.restaurant
    form_obj_user = LoginTableEditForm(instance=user_obj)
    form_obj_restaurant = RestaurantForm(instance=restaurant_obj)
    form_obj_password = PasswordChangeForm()
    if request.method == 'GET':        
        return render(request, 'restaurants/restaurant_edit_profile.html', 
                    {'user':user_obj, 'form_user':form_obj_user, 'form_res':form_obj_restaurant, 'form_password':form_obj_password})
    elif request.method == 'POST':
        form_obj_user = LoginTableEditForm(request.POST, instance=user_obj)
        form_obj_restaurant = RestaurantForm(request.POST, request.FILES, instance=user_obj.restaurant)

        # Check if both password fields are filled
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        password_fields_filled = new_password and confirm_password

        # If user is trying to change password, bind the password form
        if password_fields_filled:
            form_obj_password = PasswordChangeForm(request.POST)
        else:
            form_obj_password = PasswordChangeForm()  # unbound = won't validate or raise errors
        
        if form_obj_user.is_valid() and form_obj_restaurant.is_valid():
            form_obj_user.save()
            form_obj_restaurant.save()

            # Handle password update only if both fields filled and valid
            if password_fields_filled and form_obj_password.is_valid():
                new_password = form_obj_password.cleaned_data['new_password']
                request.user.set_password(new_password)
                request.user.save()

            return redirect('restaurant_profile')  # Redirect to the same profile page after saving

    return render(request, 'restaurants/restaurant_profile.html', {
        'form_user': form_obj_user,
        'form_res': form_obj_restaurant,
        'user': user_obj
    })