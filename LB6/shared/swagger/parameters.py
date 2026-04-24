from LB6.shared.enums.weather_api import WEATHER_API_ENUM
from LB6.shared.utils.city_coordinates import CityCoordinates

PROVIDER_PARAM = {
    "name": "provider",
    "in": "query",
    "type": "string",
    "required": True,
    "enum": WEATHER_API_ENUM,
    "default": "openweather",
    "description": "Weather provider API"
}

CITY_PARAM = {
    "name": "city",
    "in": "query",
    "type": "string",
    "required": False,
    "enum": CityCoordinates.get_cities_list(),
    "description": "City name (optional)"
}

LAT_PARAM = {
    "name": "lat",
    "in": "query",
    "type": "string",
    "required": False,
    "default": "53.9006",
    "description": "Latitude"
}

LON_PARAM = {
    "name": "lon",
    "in": "query",
    "type": "string",
    "required": False,
    "default": "27.5590",
    "description": "Longitude"
}
