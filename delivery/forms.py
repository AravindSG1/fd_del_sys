from django import forms
from .models import *

class DeliveryAgentProfileForm(forms.ModelForm):
    """Form definition for DeliveryAgentProfile."""

    class Meta:
        """Meta definition for DeliveryAgentProfileform."""

        model = DeliveryAgentProfile
        fields = ('phone', 'address', 'profile_pic')

class DeliveryAssignmentForm(forms.ModelForm):  #for updating status
    """Form definition for DeliveryAssignment."""

    class Meta:
        """Meta definition for DeliveryAssignmentform."""

        model = DeliveryAssignment
        fields = ('status',)
