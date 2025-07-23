from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import *
from .forms import *
from core.views import homepage
from orders.models import Cart, CartItem, Order, OrderItem
from orders.forms import CheckoutForm
from restaurants.models import Restaurant, FoodItem
from payments.forms import PaymentForm
from datetime import datetime
import random
from django.db.models import Q
from django.contrib.auth.decorators import login_required #for login to work on all pages
from django.contrib.auth import login

# Create your views here.
#---------------------------------------Registration Form-----------------------------------------------------
def customer_form(request):
    if request.method == 'GET':
        form_obj_user = LoginTableForm()
        form_obj_customer = CustomerProfileForm()
        return render(request,'customers/customer_form.html', {'user':form_obj_user, 'customer':form_obj_customer})
    
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST)
        form_obj_customer = CustomerProfileForm(request.POST, request.FILES)        
        if form_obj_user.is_valid() and form_obj_customer.is_valid():
            print('after if condition')
            #save the logintable            
            form_obj_user = form_obj_user.save(commit = False)  #from this line it changes from form instance to model instance
            form_obj_user.is_customer = True   #assigning role
            form_obj_user.set_password(form_obj_user.password)  #hashing password
            form_obj_user.save()

            #save customer profile 
            form_obj_customer = form_obj_customer.save(commit= False)
            form_obj_customer.customer = form_obj_user   #link to logintable instance
            form_obj_customer.save()

            cart_obj = Cart()          #creating an associated cart object to customer
            cart_obj.customer = form_obj_user
            cart_obj.save()  
            login(request, form_obj_user)        
        return redirect(customer_homepage)
    
    else:
        return redirect(homepage)

 #---------------------------------------------Home------------------------------------------------------   
@login_required(login_url='login_page')
def customer_homepage(request):    
    user_obj = request.user
    last_order_obj = request.user.order_set.filter(status='delivered').order_by('-placed_at').first()
    current_order = user_obj.order_set.filter(status__in=['pending', 'preparing', 'ready', 'out_of_delivery'],
                                              payment__status = 'success')

    #Find pending orders without a Payment object (OneToOne not created yet)
    unpaid_pending_orders = user_obj.order_set.filter(status='pending').filter(
                         Q(payment__isnull=True) | Q(payment__status='failed'))

    return render(request, 'customers/customer_homepage.html', 
                  {'user':user_obj, 'orders':current_order, 'last_order':last_order_obj,
                   'unpaid_pending': unpaid_pending_orders,})

@login_required(login_url='login_page')
def delete_order(request, id):
    order_obj = Order.objects.get(id=id)
    order_obj.delete()
    if request.user.is_superuser:
        from adminpanel.views import admin_orders
        return redirect(admin_orders)
    else:
        return redirect(customer_homepage)
    
@login_required(login_url='login_page')
def cancel_order(request, id):
    order_obj = Order.objects.get(id=id)
    order_obj.status = 'cancelled'
    order_obj.save()

    from delivery.models import DeliveryAssignment
    # Also cancel the assignment if it exists
    try:
        assignment = DeliveryAssignment.objects.get(order=order_obj)
        assignment.status = 'cancelled'
        assignment.save()
    except DeliveryAssignment.DoesNotExist:
        pass
    return redirect(customer_homepage)

#----------------------------------------Menu and Cart--------------------------------------------------------    
@login_required(login_url='login_page')
def customer_menu(request):
    if request.method == 'GET':
        user_obj = request.user
        restaurants_obj = Restaurant.objects.all()
        return render(request, 'customers/customer_menu.html', 
                      {'restaurants':restaurants_obj, 'user':user_obj})
    elif request.method == 'POST':
        user_obj = request.user
        name = request.POST['name']
        print('filter test ===================================',name)
        filtered_fooditems_obj = FoodItem.objects.filter(name__icontains = name)
        filtered_restaurants_obj = Restaurant.objects.filter(restaurant_name__icontains =name)
        return render(request, 'customers/customer_menu.html', 
                      {'restaurants':filtered_restaurants_obj, 'fooditems':filtered_fooditems_obj,
                        'user':user_obj})

@login_required(login_url='login_page')
def inside_restaurant(request, id):
    if request.method == 'GET':
        request.session['current_restaurant_id'] = id #for future reference
        user_obj = request.user
        restaurant_obj = Restaurant.objects.get(id=id)
        food_items_obj = restaurant_obj.food_items.all()  #gives queryset of all food items
        cart_obj = request.user.cart
        print(cart_obj, ' cart object')
        return render(request, 'customers/inside_restaurant.html', 
                    {'restaurant':restaurant_obj, "food_items":food_items_obj, 'cart':cart_obj, 'user':user_obj})

    elif request.method == 'POST':
        request.session['current_restaurant_id'] = id #for future reference
        user_obj = request.user
        name = request.POST['name']
        restaurant_obj = Restaurant.objects.get(id=id)
        food_items_obj = restaurant_obj.food_items.filter(name__icontains=name)  #gives queryset of all food items
        cart_obj = request.user.cart
        print(cart_obj, ' cart object')
        return render(request, 'customers/inside_restaurant.html', 
                    {'restaurant':restaurant_obj, "food_items":food_items_obj, 'cart':cart_obj, 'user':user_obj})

@login_required(login_url='login_page')
def add_on_cart(request, id):
    user_obj = request.user
    food_id = request.POST['food_id']
    quantity = request.POST['quantity']
    food_obj = FoodItem.objects.get(id=food_id)
    cart_obj = user_obj.cart
    #checking if adding from the same restaurant
    print(cart_obj.items==None,cart_obj.items.all().count()==0,'---------tst--------')
    if cart_obj.items.all().exists(): #checking if there are already items in cart
        print('checkpoint1-----------------')
        #below comparing if current food item and firstly added food item is from same restaurant
        if food_obj.restaurant.id == cart_obj.items.all()[0].food_item.restaurant.id:
            print('checkpoint2-----------------')
            #check if same food item is already added
            for cart_item in cart_obj.items.all():
                if cart_item.food_item == food_obj:
                    cart_item.quantity += int(quantity)
                    cart_item.save()
                    return redirect(inside_restaurant, id=id)
                else:
                    continue
                    
            CartItem.objects.create(cart=cart_obj, food_item=food_obj, quantity=quantity)
            return redirect(inside_restaurant, id=id)
        else:
            return redirect(customer_cart)
    else:
        CartItem.objects.create(cart=cart_obj, food_item=food_obj, quantity=quantity)
        return redirect(inside_restaurant, id=id)

@login_required(login_url='login_page')
def customer_cart(request):   
    user_obj = request.user
    cart_obj = user_obj.cart
    print(cart_obj)
    total_amount = cart_obj.total()
    cart_items = cart_obj.items.all()
    try: 
        restaurant=cart_items[0].food_item.restaurant
    except IndexError:
        restaurant=None
    return render(request, 'customers/customer_cart.html', 
                  {'user':user_obj, 'total':total_amount, 'items':cart_items, 'restaurant':restaurant})

@login_required(login_url='login_page')
def delete_cart_item(request, id):
    item_obj = CartItem.objects.get(id=id)
    item_obj.delete()
    return redirect(customer_cart)

@login_required(login_url='login_page')
def order_confirmation(request):
    user_obj = request.user
    cart_obj = user_obj.cart
    total_amount = cart_obj.total()
    cart_items = cart_obj.items.all() 
    try:
        restaurant_obj = cart_items[0].food_item.restaurant
    except IndexError:
        return redirect(customer_cart)
    if request.method == 'GET':
        form_obj = CheckoutForm()   #Order model to fill special instructions  
        return render(request, 'customers/order_confirmation.html',
                    {'user':user_obj, 'total':total_amount, 'items':cart_items, 'form':form_obj})
    
    elif request.method == 'POST':
        form_obj = CheckoutForm(request.POST)
        if form_obj.is_valid():
            order_obj = form_obj.save(commit=False)
            order_obj.customer = user_obj
            order_obj.restaurant = restaurant_obj
            order_obj.total_amount = cart_obj.total()
            order_obj.save()   

            for item in cart_obj.items.all():
                orderitem_obj = OrderItem.objects.create(order=order_obj, food_item=item.food_item, 
                                                         quantity=item.quantity, price=item.food_item.price)
                
            orderitems = order_obj.items.all()
            cart_obj.items.all().delete()  #clearing cart objects

            # payment_form_obj = PaymentForm()
            request.session['order_id'] = order_obj.id

            return redirect(payment_confirmation)
        else:
            return redirect(order_confirmation)
        
@login_required(login_url='login_page')
def payment_confirmation(request):
    order_id = request.session['order_id']
    order_obj = Order.objects.get(id= order_id)
    if request.method == 'GET':
        items = order_obj.items.all()
        payment_form_obj = PaymentForm()
        return render(request, 'customers/payment_confirmation.html', 
                      {'form':payment_form_obj, 'items':items, 'order':order_obj})
    elif request.method == 'POST':
        action = request.POST['action']
        if action == 'success':            
            form_obj = PaymentForm(request.POST)
            if form_obj.is_valid():
                payment_obj = form_obj.save(commit=False)
                payment_obj.order = order_obj
                payment_obj.amount = order_obj.total_amount
                payment_obj.txn_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
                payment_obj.status = 'success'
                payment_obj.save()

            print(order_obj)
            return render(request, 'customers/payment_success.html', {
                    'order': order_obj,
                    'txn': payment_obj
                    })
        elif action == 'delete':
            order_obj.delete()
            return redirect(customer_homepage)
        else:
            form_obj = PaymentForm(request.POST)
            payment_obj = form_obj.save(commit=False)
            payment_obj.order = order_obj
            payment_obj.amount = order_obj.total_amount
            payment_obj.txn_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
            payment_obj.status = 'failed'
            payment_obj.save()
            return redirect(customer_homepage)
    
#-----------------------------------------Orders-----------------------------------------------------------
@login_required(login_url='login_page')
def customer_orders(request):
    user_obj = request.user
    orders = user_obj.order_set.filter(status__in=['delivered','cancelled']).order_by('-updated_at')
    return render(request, 'customers/customer_orders.html', {'user':user_obj, 'orders':orders})
    
#----------------------------------------Profile--------------------------------------------------------------
@login_required(login_url='login_page')
def customer_profile(request):
    user_obj = request.user    
    return render(request, 'customers/customer_profile.html', {'user':user_obj})

@login_required(login_url='login_page')
def customer_edit_profile(request):    
    form_obj_user = LoginTableEditForm(instance=request.user)
    form_obj_password = PasswordChangeForm()
    form_obj_customer = CustomerProfileForm(instance=request.user.customerprofile)
    if request.method == 'GET':
        return render(request, 'customers/customer_edit_profile.html', 
                    {'form_user':form_obj_user, 'form_password':form_obj_password, 'form_customer':form_obj_customer})
    elif request.method == 'POST':
        form_obj_user = LoginTableEditForm(request.POST, instance=request.user)
        form_obj_customer = CustomerProfileForm(request.POST, request.FILES, instance=request.user.customerprofile)
        
        # Check if both password fields are filled
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        password_fields_filled = new_password and confirm_password

        # If user is trying to change password, bind the password form
        if password_fields_filled:
            form_obj_password = PasswordChangeForm(request.POST)
        else:
            form_obj_password = PasswordChangeForm()  # unbound = won't validate or raise errors
        
        #saving other two forms
        if form_obj_user.is_valid() and form_obj_customer.is_valid():
            form_obj_user.save()
            form_obj_customer.save()

            # Handle password update only if both fields filled and valid
            if password_fields_filled and form_obj_password.is_valid():
                new_password = form_obj_password.cleaned_data['new_password']
                request.user.set_password(new_password)
                request.user.save()

            #Set and hash the password
            # new_password = form_obj_password.cleaned_data['new_password']
            # request.user.set_password(new_password)
            # request.user.save()
            
            return redirect('customer_profile')  # Redirect to the same profile page after saving

    return render(request, 'customers/customer_profile.html', {
        'form_user': form_obj_user,
        'form_res': form_obj_customer,        
    })