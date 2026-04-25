from decimal import Decimal
from typing import Tuple, Optional

import requests

from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.forecast.get import Forecast


class GoogleWeatherClient(WeatherDataClient):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_current_weather(self, lat: Decimal, lon: Decimal) -> Tuple[Decimal, Optional[Exception]]:
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

    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        url = f"{self.base_url}/forecast/days:lookup?key={self.api_key}&location.latitude={lat}&location.longitude={lon}&days=5"

        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Forecast([]), Exception(f"google weather returned bad status: {resp.status_code}")
            data = resp.json()

            days = data.get('forecastDays', [])[:5]
            if not days:
                return Forecast([]), Exception("bad data from googleweather")

            temps = []
            for day in days:
                max_temp = day.get('maxTemperature')
                if not max_temp or 'degrees' not in max_temp:
                    return Forecast([]), Exception("bad data from googleweather")

                temps.append(Decimal(str(max_temp['degrees'])))
            return Forecast(temps), None
        except (KeyError, ValueError) as e:
            return Forecast([]), Exception(f"failed to decode response: {e}")
        except Exception as e:
            return Forecast([]), Exception(f"failed to get google forecast: {e}")
