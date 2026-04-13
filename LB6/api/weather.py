from flask import request, jsonify
from controllers.weather import CurrentWeatherController
from clients.openweather import OpenWeatherClient
from shared.utils.env import get_env
from shared.responses.status import StatusResponse
from shared.responses.success import SuccessResponse
from models.weather.get import CurrentWeather
from decimal import Decimal

class WeatherHandler:
    def __init__(self):
        api_key = get_env("OPENWEATHER_API_KEY", "")
        base_url = get_env("OPENWEATHER_BASE_URL", "")
        client = OpenWeatherClient(api_key, base_url)
        self.controller = CurrentWeatherController(client)
    
    def handle_get_current_weather(self):
        try:
            lat_str = request.args.get('lat')
            lon_str = request.args.get('lon')
            
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
