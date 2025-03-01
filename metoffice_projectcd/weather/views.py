from rest_framework import viewsets
from .models import WeatherData
from .serializers import WeatherDataSerializer

class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
