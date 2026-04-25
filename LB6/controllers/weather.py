from decimal import Decimal
from typing import Tuple, Optional, List

from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather


class WeatherController:
    def __init__(self, client: WeatherDataClient):
        self.client = client

    def get_current_weather(self, lat: Decimal, lon: Decimal) -> Tuple[Weather, Optional[Exception]]:
        temperature, err = self.client.get_current_weather(lat, lon)
        if err:
            return Weather(Decimal('0')), err

        return Weather(temperature), None

    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        forecast, err = self.client.get_forecast(lat, lon)
        if err:
            return Forecast([]), err
        return forecast, None

    def get_multiple_weather(
            self,
            locations: List[Tuple[Decimal, Decimal]]
    ) -> Tuple[List[Weather], Optional[Exception]]:
        temps = []
        for lat, lon in locations:
            temp, err = self.get_current_weather(lat, lon)
            if err:
                return [], err
            temps.append(temp)

        return temps, None
