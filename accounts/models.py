from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class LoginTable(AbstractUser):
    is_customer = models.BooleanField(default=0)
    is_restaurant = models.BooleanField(default=0)
    is_delivery = models.BooleanField(default=0)