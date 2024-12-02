import json
from django.core.management.base import BaseCommand
from properties.models import Location
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Generate sitemap.json for all country locations"

    def handle(self, *args, **kwargs):
        sitemap = []

        # Fetch all countries from the Location model
        countries = Location.objects.filter(location_type="country").order_by("title")
        for country in countries:
            country_slug = slugify(country.title)
            country_data = {
                country.title: country_slug,
                "locations": []
            }

            # Fetch child locations (states or cities) of the country
            child_locations = Location.objects.filter(parent=country).order_by("title")
            for location in child_locations:
                location_slug = slugify(location.title)
                # If the location is a state, fetch its cities as well
                if location.location_type == 'state':
                    state_data = {
                        location.title: f"{country_slug}/{location_slug}",
                        "cities": []
                    }
                    cities = Location.objects.filter(parent=location).order_by("title")
                    for city in cities:
                        city_slug = slugify(city.title)
                        state_data["cities"].append({
                            city.title: f"{country_slug}/{location_slug}/{city_slug}"
                        })
                    country_data["locations"].append(state_data)
                else:
                    country_data["locations"].append({
                        location.title: f"{country_slug}/{location_slug}"
                    })

            sitemap.append(country_data)

        # Save to sitemap.json
        with open("sitemap.json", "w") as file:
            json.dump(sitemap, file, indent=4)

        self.stdout.write(self.style.SUCCESS("Sitemap generated successfully!"))
