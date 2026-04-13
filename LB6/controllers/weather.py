from decimal import Decimal
from typing import Tuple, Optional
from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.weather.get import CurrentWeather

class CurrentWeatherController:
    def __init__(self, client: WeatherDataClient):
        self.client = client
    
    def get_current_weather(self, lat: Decimal, lon: Decimal) -> Tuple[CurrentWeather, Optional[Exception]]:
        temperature, err = self.client.location_current_temperature(lat, lon)
        if err:
            return CurrentWeather(Decimal('0')), err
        
        return CurrentWeather(temperature), None
