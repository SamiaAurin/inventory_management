from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth.models import User
from .models import Location, Accommodation, LocalizeAccommodation
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields



class LocationResource(resources.ModelResource):
    # Define custom field for center (Point)
    center = fields.Field()

    class Meta:
        model = Location
        fields = ('id', 'title', 'center', 'parent', 'location_type', 'country_code', 'state_abbr', 'city')
        export_order = ('id', 'title', 'center', 'parent', 'location_type', 'country_code', 'state_abbr', 'city')

    def before_import_row(self, row, **_kwargs):
        
        if "center" in row and row["center"]:
            try:
                if 'POINT(' in row["center"]:
                    coordinates = row["center"].replace("POINT(", "").replace(")", "").split()
                    longitude, latitude = map(float, coordinates)
                else:
                    latitude, longitude = map(float, row["center"].split(','))
                row["center"] = Point(longitude, latitude, srid=4326)
            except ValueError as e:
                raise ValidationError(f"Invalid center format: {row['center']}. Error: {str(e)}")
        
        return row



# Register the model with import-export functionality
@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, LeafletGeoAdmin):
    
    resource_class = LocationResource  # Link the resource class to the admin
    list_display = ('title', 'location_type', 'country_code', 'created_at')
    list_filter = ('location_type', 'country_code')
    search_fields = ('title', 'city')
    
    
             
# Custom form for the Accommodation admin interface
class AccommodationAdminForm(forms.ModelForm):
    user = forms.CharField(max_length=150, label="Username/UserID", disabled=True)  # Text input for username
   
    class Meta:
        model = Accommodation
        fields = '__all__'
       
    # Custom validation for user field, only if not auto-filled
    def clean_user(self):
        # If the user is pre-filled, we don't need to validate it
        username = self.cleaned_data.get('user')
        if username:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                raise ValidationError("User with this username does not exist.")
        return None

# Custom admin for Accommodation model

class AccommodationAdmin(LeafletGeoAdmin):
    form = AccommodationAdminForm  # Use the custom form with the user field

    # List the fields to display in the admin
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'location', 'published', 'user')
    search_fields = ('title', 'country_code', 'location', 'user')

    # Read-only fields for admin
    readonly_fields = ('user',)  # Make the user field read-only in the admin

    # Filter accommodations based on the logged-in user
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # If user is not a superuser, filter by the logged-in user
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)  # Filter by logged-in user
        
        return queryset

    # Auto-fill user during save
    def save_model(self, request, obj, form, change):
        if not obj.user:  # Ensure user is set only if not already set
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Register the model and admin
admin.site.register(Accommodation, AccommodationAdmin)



@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description')
    list_filter = ('language', 'property')
    search_fields = ('property', 'language', 'description')