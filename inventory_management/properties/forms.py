from django import forms
from .models import Accommodation, Location

class AccommodationForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all())

    class Meta:
        model = Accommodation
        fields = [
            'title', 'country_code', 'bedroom_count', 
            'usd_rate', 'location', 'amenities', 'images'
        ]
        widgets = {
            'amenities': forms.TextInput(),
            'images': forms.TextInput(),
        }