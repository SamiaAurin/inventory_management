from django.contrib import admin
from django.contrib.gis.forms import PointField
from leaflet.admin import LeafletGeoAdmin
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.models import User
from .models import Location, Accommodation, LocalizeAccommodation
from django import forms
from django.core.exceptions import ValidationError


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('title', 'location_type', 'country_code', 'created_at')
    list_filter = ('location_type', 'country_code')
    search_fields = ('title', 'city')
    
# Custom form for the Accommodation admin interface
class AccommodationAdminForm(forms.ModelForm):
    user = forms.CharField(max_length=150, label="Username")  # Text input for username
   
    class Meta:
        model = Accommodation
        fields = '__all__'
       
    def clean_user(self):
        username = self.cleaned_data.get('user')
        try:
            user = User.objects.get(username=username)  # Lookup user by username
            return user
        except User.DoesNotExist:
            raise ValidationError("User with this username does not exist.")

# Custom admin for Accommodation model
class AccommodationAdmin(LeafletGeoAdmin):
    form = AccommodationAdminForm  # Use custom form

    # List the fields to display in the admin
    list_display = ('title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'location', 'published', 'user')

    # Filter accommodations based on the logged-in user
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # If user is not a superuser, filter by the logged-in user
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)  # Filter by logged-in user
        
        return queryset

admin.site.register(Accommodation, AccommodationAdmin)


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language')
    list_filter = ('language',)