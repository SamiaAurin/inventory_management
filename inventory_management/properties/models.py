from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import connection
import pycountry

class Location(models.Model):
    LOCATION_TYPES = [
        ('continent', 'Continent'),
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField(geography=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    country_code = models.CharField(max_length=2, blank=True)
    state_abbr = models.CharField(max_length=3, blank=True)
    city = models.CharField(max_length=30, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        # Validation for hierarchy and country codes
        if self.country_code:
             country = pycountry.countries.get(alpha_2=self.country_code.upper())
             if not country:
                raise ValidationError(f"{self.country_code} is not a valid ISO country code.")

        if self.state_abbr and len(self.state_abbr) > 2:
            raise ValidationError("State abbreviation must be at most 2 characters.")

    def __str__(self):
        return self.title

class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.PointField(geography=True, null=True, blank=True)
    images = models.JSONField(default=list)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.title



class LocalizeAccommodation(models.Model):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = models.JSONField(default=dict)

    class Meta:
        unique_together = ('property', 'language')

    def save(self, *args, **kwargs):
        # Insert or update the appropriate partition based on language
        partition_table = f'localizeaccommodation_{self.language}'
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {partition_table} (property_id, language, description, policy)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (property_id, language) 
                DO UPDATE SET description = EXCLUDED.description, policy = EXCLUDED.policy;
            """, [self.property.id, self.language, self.description, self.policy])

