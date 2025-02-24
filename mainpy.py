import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from weather.models import WeatherData

class Command(BaseCommand):
    help = 'Fetch weather data from UK MetOffice and store it'

    def handle(self, *args, **kwargs):
        url = 'https://api.metoffice.gov.uk/val/wxfcs/all/json/sitelist?res=3hourly&key=' + settings.METOFFICE_API_KEY
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            for site in data['Locations']['Location']:
                WeatherData.objects.update_or_create(
                    location_id=site['id'],
                    defaults={'name': site['name'], 'region': site['region']}
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored weather data'))
        else:
            self.stderr.write(self.style.ERROR('Failed to fetch data'))
