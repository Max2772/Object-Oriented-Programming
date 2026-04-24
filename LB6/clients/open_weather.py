from typing import List, Tuple, Optional

import requests
from decimal import Decimal
from LB6.clients.weather_data_client import WeatherDataClient
from LB6.models.forecast.get import Forecast


class OpenWeatherClient(WeatherDataClient):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    def location_current_temperature(self, lat: Decimal, lon: Decimal):
        url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Decimal('0'), Exception(f"openweather returned bad status: {resp.status_code}")
            
            data = resp.json()
            temp = Decimal(str(data['main']['temp']))
            return temp, None
        except requests.RequestException as e:
            return Decimal('0'), Exception(f"failed to call openweather: {e}")
        except (KeyError, ValueError) as e:
            return Decimal('0'), Exception(f"failed to decode response: {e}")

    def get_current_temperatures(self, locations: List[Tuple[Decimal, Decimal]]) -> Tuple[List[Decimal], Optional[Exception]]:
        temps = []
        for lat, lon in locations:
            temp, err = self.location_current_temperature(lat, lon)
            if err:
                return [], err
            temps.append(temp)
        return temps, None

    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"

        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Forecast([]), Exception(f"openweather returned bad status: {resp.status_code}")
            data = resp.json()
            forecasts = data.get('list', [])
            temps = []

            step = 8 if len(forecasts) >= 40 else 1

            for i in range(0, len(forecasts), step):
                item = forecasts[i].get('main', {}).get('temp')
                if item is not None:
                    temp = Decimal(str(item))
                    temps.append(temp)
            return Forecast(temps), None
        except Exception as e:
            return Forecast([]), Exception(f"failed to get openweather forecast: {e}")