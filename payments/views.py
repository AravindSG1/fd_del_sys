from django.shortcuts import render
from django.http import HttpResponse
from orders.models import Order
from payments.forms import *
import random

# Create your views here.
