from django import forms
from .models import *

class LoginTableForm(forms.ModelForm):
    """Form definition for LoginTable."""

    class Meta:
        """Meta definition for LoginTableform."""

        model = LoginTable
        fields = ('username', 'password','email')

class LoginTableEditForm(forms.ModelForm):
    """Form definition for LoginTableEdit."""

    class Meta:
        """Meta definition for LoginTableEditform."""

        model = LoginTable
        fields = ('username', 'email')


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password', required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data