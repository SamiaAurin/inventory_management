from django import forms
from django.contrib.auth.models import User
from .models import Accommodation

# Signup form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Property creation form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'images', 'amenities']
