from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Accommodation, Location
from .forms import AccommodationForm

def property_list(request):
    properties = Accommodation.objects.filter(published=True)
    return render(request, 'properties/property_list.html', {'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()
            return redirect('property_list')
    else:
        form = AccommodationForm()
    return render(request, 'properties/property_create.html', {'form': form})

def property_detail(request, property_id):
    property_instance = Accommodation.objects.get(id=property_id)
    return render(request, 'properties/property_detail.html', {'property': property_instance})
