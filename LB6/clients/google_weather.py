import requests
from decimal import Decimal
from typing import List, Tuple, Optional

from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.forecast.get import Forecast


class GoogleWeatherClient(WeatherDataClient):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def location_current_temperature(self, lat: Decimal, lon: Decimal) -> Tuple[Decimal, Optional[Exception]]:
        url = f"{self.base_url}/currentConditions:lookup?key={self.api_key}&location.latitude={lat}&location.longitude={lon}"

        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Decimal('0'), Exception(f"google weather returned bad status: {resp.status_code}")

            data = resp.json()
            temp = Decimal(str(data['temperature']['degrees']))
            return temp, None
        except requests.RequestException as e:
            return Decimal('0'), Exception(f"failed to call google weather: {e}")
        except (KeyError, ValueError, TypeError) as e:
            return Decimal('0'), Exception(f"failed to decode google response: {e}")

    def get_current_temperatures(self, locations: List[Tuple[Decimal, Decimal]]) -> Tuple[List[Decimal], Optional[Exception]]:
        temps = []
        for lat, lon in locations:
            temp, err = self.location_current_temperature(lat, lon)
            if err:
                return [], err
            temps.append(temp)
        return temps, None

    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        url = f"{self.base_url}/forecast/days:lookup?key={self.api_key}&location.latitude={lat}&location.longitude={lon}&days=5"

        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Forecast([]), Exception(f"google weather forecast returned bad status: {resp.status_code}")
            data = resp.json()
            temps = []
            for day in data.get('forecastDays', [])[:5]:
                if 'maxTemperature' in day:
                    temp = Decimal(str(day['maxTemperature']['degrees']))
                    temps.append(temp)
            return Forecast(temps), None
        except Exception as e:
            return Forecast([]), Exception(f"failed to get google forecast: {e}")