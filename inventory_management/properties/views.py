from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Accommodation
from .forms import PropertyForm, SignupForm  # Assuming you have forms for property creation and signup

# Signup view for property owners
def property_owner_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set hashed password
            user.save()

            # Add the user to the 'Property Owners' group
            group, created = Group.objects.get_or_create(name='Property Owners')
            user.groups.add(group)

            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('properties:login')  # Redirect to login page
    else:
        form = SignupForm()

    return render(request, 'properties/signup.html', {'form': form})



