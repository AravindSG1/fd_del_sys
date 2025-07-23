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
    path('', admin_dashboard, name='admin_dashboard'),
    path('restaurant_approval/<int:id>/', restaurant_approval, name='restaurant_approval'),
    path('restaurant_details/<int:id>/', restaurant_details, name='restaurant_details'), 
    path('restaurant_edit/<int:id>/', restaurant_edit, name='restaurant_edit'),   
    path('delete_restaurant/<int:id>/', delete_restaurant, name='delete_restaurant'),  

    path('admin_manage_users/', admin_manage_users, name='admin_manage_users'),
    path('customer_details/<int:id>/', customer_details, name='customer_details'),    
    path('customer_edit/<int:id>/', customer_edit, name='customer_edit'),
    path('delete_customer/<int:id>/', delete_customer,name='delete_customer'),

    path('admin_restaurants/', admin_restaurants, name='admin_restaurants'),
    path('admin_orders/', admin_orders, name='admin_orders'),
    path('admin_payments/', admin_payments, name='admin_payments'),
    path('admin_delivery_agents/', admin_delivery_agents, name='admin_delivery_agents'),
    path('delivery_agent_details/<int:id>/', delivery_agent_details, name='delivery_agent_details'),
    path('delivery_agent_edit/<int:id>/', delivery_agent_edit, name='delivery_agent_edit'),
    path('delete_delivery_agents/<int:id>/', delete_delivery_agents,name='delete_delivery_agents'),
]
