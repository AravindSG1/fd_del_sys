from django import forms
from .models import *

class CustomerProfileForm(forms.ModelForm):
    """Form definition for CustomerProfile."""

    class Meta:
        """Meta definition for CustomerProfileform."""

        model = CustomerProfile
        fields = ('phone', 'address', 'profile_pic',)