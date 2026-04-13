from decimal import Decimal
from typing import Tuple, Optional
from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather

class CurrentWeatherController:
    def __init__(self, client: WeatherDataClient):
        self.client = client
    
    def get_current_weather(self, lat: Decimal, lon: Decimal) -> Tuple[Weather, Optional[Exception]]:
        temperature, err = self.client.location_current_temperature(lat, lon)
        if err:
            return Weather(Decimal('0')), err
        
        return Weather(temperature), None

    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        forecast, err = self.client.get_forecast(lat, lon)
        if err:
            return Forecast([]), err
        return forecast, None
