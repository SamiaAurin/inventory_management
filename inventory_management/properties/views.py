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

    return render(request, 'signup.html', {'form': form})

# List properties (only for logged-in users)
@login_required
def property_list(request):
    properties = Accommodation.objects.filter(user=request.user)  # Show only properties owned by the logged-in user
    return render(request, 'property_list.html', {'properties': properties})

# Create a property (only for logged-in users)
@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)  # Assuming you allow file uploads for property images
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user  # Assign the current user as the owner
            property_instance.save()
            messages.success(request, 'Property created successfully!')
            return redirect('properties:property_list')
    else:
        form = PropertyForm()

    return render(request, 'property_create.html', {'form': form})

# View property details (only for logged-in users)
@login_required
def property_detail(request, property_id):
    property_instance = get_object_or_404(Accommodation, id=property_id, user=request.user)  # Restrict to properties owned by the user
    return render(request, 'property_detail.html', {'property': property_instance})
