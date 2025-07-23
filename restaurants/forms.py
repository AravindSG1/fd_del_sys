from django import forms
from .models import *
from orders.models import Order

class RestaurantForm(forms.ModelForm):
    """Form definition for Restaurant."""

    class Meta:
        """Meta definition for Restaurantform."""

        model = Restaurant
        fields = ('restaurant_name', 'address', 'phone', 'restaurant_email', 'logo', 'description',)

class FoodItemForm(forms.ModelForm):
    """Form definition for FoodItem."""

    class Meta:
        """Meta definition for FoodItemform."""

        model = FoodItem
        fields = ('category', 'name', 'description', 'price', 'image', 'is_available')
        # fields = '__all__'

class ReceivedOrderForm(forms.ModelForm):
    """Form definition for RecievedOrder."""

    class Meta:
        """Meta definition for RecievedOrderform."""

        model = Order
        fields = ('status',)
