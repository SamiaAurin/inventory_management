from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from .models import Location, Accommodation, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(GeoModelAdmin):
    list_display = ('title', 'location_type', 'country_code', 'created_at')
    list_filter = ('location_type', 'country_code')
    search_fields = ('title', 'city')
    
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_code', 'bedroom_count', 'review_score', 'published')
    list_filter = ('country_code', 'bedroom_count', 'published')
    search_fields = ('title',)

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language')
    list_filter = ('language',)