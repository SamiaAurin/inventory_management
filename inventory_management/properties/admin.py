from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth.models import User
from .models import Location, Accommodation, LocalizeAccommodation
from django import forms
from django.core.exceptions import ValidationError
from django.db import connection, IntegrityError

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
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
    list_display = ('property', 'language')
    list_filter = ('language', 'property')
    def save_model(self, request, obj, form, change):
        # Manually set the partition for the correct language
        partition_table = f'localizeaccommodation_{obj.language}'
        
        # Ensure the property_id exists in the properties_accommodation table
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM properties_accommodation WHERE id = %s", [obj.property_id])
            result = cursor.fetchone()
            if result[0] == 0:
                raise IntegrityError(f"Property with id {obj.property_id} does not exist in properties_accommodation.")
            
            try:
                cursor.execute(f"""
                    INSERT INTO {partition_table} (property_id, language, description, policy)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (property_id, language) 
                    DO UPDATE SET description = EXCLUDED.description, policy = EXCLUDED.policy;
                """, [obj.property_id, obj.language, obj.description, obj.policy])
            except IntegrityError as e:
                raise IntegrityError(f"Error inserting data into partition: {e}")