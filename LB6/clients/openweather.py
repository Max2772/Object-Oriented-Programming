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

    def get_forecast(self, lat: Decimal, lon: Decimal):
        url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Forecast([]), Exception(f"openweather forecast returned bad status: {resp.status_code}")
            data = resp.json()
            temps = []
            for i in range(0, 40, 8):
                if i < len(data.get('list', [])):
                    temp = Decimal(str(data['list'][i]['main']['temp']))
                    temps.append(temp)
            return Forecast(temps), None
        except Exception as e:
            return Forecast([]), Exception(f"failed to get openweather forecast: {e}")