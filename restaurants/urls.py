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
    path('restaurant_form/',restaurant_form, name='restaurant_form'),
    
    path('restaurant_dashboard/', restaurant_dashboard, name='restaurant_dashboard'),
    path('add_food/', food_item, name='add_food'), 
    path('delete_food/<int:id>/', delete_food, name='delete_food'),
    path('edit_food/<int:id>/', edit_food, name='edit_food'),   

    path('restaurant_fooditems/', restaurant_fooditems, name='restaurant_fooditems'),
    path('restaurant_orders/', restaurant_orders, name='restaurant_orders'),
    path('restaurant_profile/', restaurant_profile, name='restaurant_profile'),
    path('restaurant_profile/edit/', restaurant_edit_profile, name='restaurant_edit_profile'),
]
