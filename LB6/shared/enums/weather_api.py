from enum import Enum


class WeatherAPI(Enum):
    OPEN_WEATHER = "openweather"
    GOOGLE_WEATHER = "googleweather"


WEATHER_API_ENUM = [api.value for api in WeatherAPI]
