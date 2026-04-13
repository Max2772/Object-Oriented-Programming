from decimal import Decimal
from typing import List, Tuple

from flask import request, jsonify

from LB6.clients.openweather import OpenWeatherClient
from LB6.controllers.weather import WeatherController
from LB6.shared.responses.status import StatusResponse
from LB6.shared.responses.success import SuccessResponse
from LB6.shared.utils.city_coordinates import CityCoordinates
from LB6.shared.utils.env import get_env


class WeatherHandler:
    def __init__(self):
        api_key = get_env("OPENWEATHER_API_KEY", "")
        base_url = get_env("OPENWEATHER_BASE_URL", "")
        client = OpenWeatherClient(api_key, base_url)
        self.controller = WeatherController(client)

    def handler_get_current_weather(self):
        try:
            lat_str = request.args.get("lat")
            lon_str = request.args.get("lon")

            if not lat_str or not lon_str:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            try:
                lat = Decimal(lat_str)
                lon = Decimal(lon_str)
            except:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            result, err = self.controller.get_current_weather(lat, lon)

            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handler_get_multiple_current_weather(self):
        try:
            raw = request.args.get("cords")
            cords_str = raw.split(",")
            if len(cords_str) % 2 != 0:
                return jsonify(StatusResponse(400, "even amount of coordinates required").to_dict()), 400
            if not cords_str:
                return jsonify(StatusResponse(400, "coordinates parameter required").to_dict()), 400

            try:
                cords = [Decimal(cord) for cord in cords_str]
            except:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            locations = []
            for lat, lon in zip(cords[::2], cords[1::2]):
                locations.append([lat, lon])

            result, err = self.controller.get_current_temperatures(locations)
            if err:
                return jsonify(StatusResponse(400, str(err)).to_dict()), 400

            data = [temp.to_dict() for temp in result]
            return jsonify(SuccessResponse(200, "Success", data).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handler_get_forecast(self):
        try:
            city = request.args.get("city")
            lat_str = request.args.get("lat")
            lon_str = request.args.get("lon")

            if city:
                if lat_str or lon_str:
                    return jsonify(StatusResponse(400, "too many arguments").to_dict()), 400

                lat_str, lon_str, err = CityCoordinates.resolve(city)
                if err:
                    return jsonify(StatusResponse(400, f"{str(err)}").to_dict()), 400

            if not lat_str or not lon_str:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            try:
                lat = Decimal(lat_str)
                lon = Decimal(lon_str)
            except:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            result, err = self.controller.get_forecast(lat, lon)

            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500
