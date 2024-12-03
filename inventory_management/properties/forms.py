from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Signup form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    # Custom validation for the username field
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check if username already exists in the database
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        
        return username