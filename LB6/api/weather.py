from decimal import Decimal

from flask import request, jsonify

from LB6.clients.google_weather import GoogleWeatherClient
from LB6.clients.open_weather import OpenWeatherClient
from LB6.controllers.weather import WeatherController
from LB6.shared.enums.weather_api import WeatherAPI
from LB6.shared.responses.status import StatusResponse
from LB6.shared.responses.success import SuccessResponse
from LB6.shared.utils.city_coordinates import CityCoordinates
from LB6.shared.utils.coordinates_validator import validate_lat_lon
from LB6.shared.utils.env import get_env


class WeatherHandler:
    def __init__(self):
        self.open_weather_key = get_env("OPENWEATHER_API_KEY", "")
        self.open_weather_url = get_env("OPENWEATHER_BASE_URL", "")
        self.google_weather_key = get_env("GOOGLE_WEATHER_API_KEY", "")
        self.google_weather_url = get_env("GOOGLE_BASE_URL", "")

    def _get_client(self, provider: WeatherAPI):
        if provider == WeatherAPI.GOOGLE_WEATHER:
            if not self.google_weather_key:
                raise ValueError("GOOGLE_WEATHER_API_KEY is not set")
            return GoogleWeatherClient(self.google_weather_key, self.google_weather_url)
        elif provider == WeatherAPI.OPEN_WEATHER:
            if not self.open_weather_key:
                raise ValueError("OPENWEATHER_API_KEY is not set")
            return OpenWeatherClient(self.open_weather_key, self.open_weather_url)
        else:
            raise ValueError("unknown provider")

    def _resolve_provider(self):
        try:
            raw_provider = request.args.get("provider")
            if not raw_provider:
                return None, StatusResponse(400, "provider argument required")

            provider = WeatherAPI(raw_provider.lower())
            return provider, None
        except ValueError:
            return None, StatusResponse(400, "invalid provider")

    def _resolve_multiple_coordinates(self):
        raw_cities = request.args.get("cities")
        raw_coords = request.args.get("coords")

        if raw_cities:
            if raw_coords:
                return None, StatusResponse(400, "too many arguments")

            cities = [c.strip().lower() for c in raw_cities.split(",")]
            locations = []
            for city in cities:
                lat, lon, err = CityCoordinates.resolve(city)
                if err:
                    return None, StatusResponse(400, f"invalid city: {city}")
                locations.append([lat, lon])

            return locations, None

        if not raw_coords:
            return None, StatusResponse(400, "not enough arguments")

        coords_str = raw_coords.split(",")
        if len(coords_str) % 2 != 0:
            return None, StatusResponse(400, "even amount of coordinates required")

        try:
            coords = [Decimal(coord) for coord in coords_str]
        except:
            return None, StatusResponse(400, "invalid coordinates")

        locations = []
        for lat, lon in zip(coords[::2], coords[1::2]):
            err = validate_lat_lon(lat, lon)
            if err:
                return None, StatusResponse(400, err)
            locations.append([lat, lon])

        return locations, None

    def _resolve_coordinates(self):
        city = request.args.get("city")
        lat_str = request.args.get("lat")
        lon_str = request.args.get("lon")

        if city:
            if lat_str or lon_str:
                return None, None, StatusResponse(400, "too many arguments")

            lat, lon, err = CityCoordinates.resolve(city)
            if err:
                return None, None, StatusResponse(400, str(err))
            return lat, lon, None

        if not lat_str or not lon_str:
            return None, None, StatusResponse(400, "not enough arguments")

        try:
            lat = Decimal(lat_str)
            lon = Decimal(lon_str)
        except:
            return None, None, StatusResponse(400, "invalid coordinates")

        err = validate_lat_lon(lat, lon)
        if err:
            return None, None, StatusResponse(400, err)

        return lat, lon, None

    def handler_get_current_weather(self):
        try:
            provider, err_response = self._resolve_provider()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            lat, lon, err_response = self._resolve_coordinates()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            client = self._get_client(provider)
            controller = WeatherController(client)
            result, err = controller.get_current_weather(lat, lon)

            if err:
                return jsonify(StatusResponse(400, str(err)).to_dict()), 400

            return jsonify(SuccessResponse(200, "success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handler_get_forecast(self):
        try:
            provider, err_response = self._resolve_provider()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            lat, lon, err_response = self._resolve_coordinates()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            client = self._get_client(provider)
            controller = WeatherController(client)
            result, err = controller.get_forecast(lat, lon)

            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handler_get_multiple_current_weather(self):
        try:
            provider, err_response = self._resolve_provider()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            locations, err_response = self._resolve_multiple_coordinates()
            if err_response:
                return jsonify(err_response.to_dict()), err_response.code

            client = self._get_client(provider)
            controller = WeatherController(client)
            result, err = controller.get_multiple_weather(locations)
            if err:
                return jsonify(StatusResponse(400, str(err)).to_dict()), 400

            data = [temp.to_dict() for temp in result]
            return jsonify(SuccessResponse(200, "success", data).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handler_get_all_cities(self):
        data = CityCoordinates.get_cities_list()
        return jsonify(SuccessResponse(200, "success", data).to_dict()), 200
