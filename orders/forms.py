from django import forms
from .models import *

class CheckoutForm(forms.ModelForm):
    """Form definition for Checkout."""

    class Meta:
        """Meta definition for Checkoutform."""

        model = Order
        fields = ('special_instructions',)
