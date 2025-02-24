import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from weather.models import WeatherData

class Command(BaseCommand):
    help = 'Fetch weather data from UK MetOffice and store it'

    def handle(self, *args, **kwargs):
        url = f"https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0/orders?detail=FULL"
        headers = {
            "apikey": f"{settings.METOFFICE_API_KEY}"
        }
        response = requests.get(url, headers)

        # Print the response status and content
        print("Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            try:
                data = response.json()
                locations = data.get('Locations', {}).get('Location', [])
                
                if not locations:
                    print("⚠️ No locations found in the response.")

                for site in locations:
                    WeatherData.objects.update_or_create(
                        location_id=site['id'],
                        defaults={
                            'name': site['name'],
                            'region': site['region'],
                        }
                    )
                self.stdout.write(self.style.SUCCESS('Successfully fetched and stored weather data'))
            except Exception as e:
                print(f"⚠️ Error parsing JSON: {e}")
        else:
            self.stderr.write(self.style.ERROR('Failed to fetch data'))
