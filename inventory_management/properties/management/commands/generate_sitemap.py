import json
from django.core.management.base import BaseCommand
from myapp.models import Country, Location

class Command(BaseCommand):
    help = "Generate sitemap.json for all country locations"

    def handle(self, *args, **kwargs):
        sitemap = []

        # Fetch countries and locations
        for country in Country.objects.all():
            country_data = {
                country.name: country.slug,
                "locations": []
            }

            # Fetch and sort locations
            locations = country.locations.order_by("name")
            for location in locations:
                country_data["locations"].append({
                    location.name: f"{country.slug}/{location.slug}"
                })

            sitemap.append(country_data)

        # Save to sitemap.json
        with open("sitemap.json", "w") as file:
            json.dump(sitemap, file, indent=4)

        self.stdout.write(self.style.SUCCESS("Sitemap generated successfully!"))
