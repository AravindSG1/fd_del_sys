from django import forms
from .models import *

class PaymentForm(forms.ModelForm):
    """Form definition for Payment."""

    class Meta:
        """Meta definition for Paymentform."""

        model = Payment
        fields = ('method',)

