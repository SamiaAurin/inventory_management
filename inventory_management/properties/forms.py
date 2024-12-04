from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Signup form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    # Custom validation for the username and email fields
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        # Check if username already exists in the database
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        
        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken. Please choose a different one.")
        
        return cleaned_data