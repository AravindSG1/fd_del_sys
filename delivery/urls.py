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
    path('delivery_agent_form/',delivery_agent_form, name='delivery_agent_form'),    
    path('delivery_agent_dashboard/', delivery_agent_dashboard, name='delivery_agent_dashboard'),
    path('delivery_agent_mydeliveries/', delivery_agent_mydeliveries, name='delivery_agent_mydeliveries'),
    path('delivery_agent_profile/', delivery_agent_profile, name='delivery_agent_profile'),
    path('delivery_agent_profile/edit/', delivery_agent_edit_profile, name='delivery_agent_edit_profile'),
]
