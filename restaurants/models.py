from django.db import models
from accounts.models import LoginTable

# Create your models here.
class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200)
    owner = models.OneToOneField(LoginTable, on_delete=models.CASCADE, related_name='restaurant') #for reverse relation
    address = models.TextField()
    phone = models.CharField(max_length=20)
    restaurant_email = models.EmailField()
    logo = models.ImageField(upload_to='restaurants/logos', blank=True, null=True)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant_name
    
class FoodItem(models.Model):
    Category_Choices = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='restaurants/food_images', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_items')
    category = models.CharField(max_length=50, choices=Category_Choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}--{self.restaurant.restaurant_name}"