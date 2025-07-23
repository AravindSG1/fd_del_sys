"""
URL configuration for fd_del_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('customer_form/',customer_form, name='customer_form'),
    path('customer_homepage/',customer_homepage, name='customer_homepage'),
    path('customer_menu/', customer_menu, name= 'customer_menu'),    
    path('inside_restaurant/<int:id>/', inside_restaurant, name='inside_restaurant'),
    path('add_on_cart/<int:id>/', add_on_cart, name='add_on_cart'),
    path('customer_cart/', customer_cart, name='customer_cart'),
    path('delete_cart_item/<int:id>/', delete_cart_item, name='delete_cart_item'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('payment_confirmation/', payment_confirmation, name='payment_confirmation'),
    path('customer_orders/', customer_orders, name='customer_orders'),
    path('customer_profile/', customer_profile, name='customer_profile'),
    path('customer_profile/edit/', customer_edit_profile, name='customer_edit_profile'),
    path('delete_order/<int:id>/', delete_order, name='delete_order'),
    path('cancel_order/<int:id>/', cancel_order, name='cancel_order'),
]
