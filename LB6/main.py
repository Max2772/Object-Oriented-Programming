from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from api.weather import WeatherHandler

load_dotenv()

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather Example API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

weather_handler = WeatherHandler()

@app.route('/api/v1/weather', methods=['GET'])
def get_current_weather():
    return weather_handler.handle_get_current_weather()

@app.route('/api/v1/forecast', methods=['GET'])
def get_forecast():
    return weather_handler.handle_get_forecast()


@app.route('/swagger.json')
def swagger():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Weather Example API",
            "version": "1.0",
            "description": ""
        },
        "basePath": "/api/v1",
        "paths": {
            "/weather": {
                "get": {
                    "summary": "Get Current Weather",
                    "description": "Returns current weather for given coordinates",
                    "tags": ["weather"],
                    "produces": ["application/json"],
                    "parameters": [
                        {
                            "name": "lat",
                            "in": "query",
                            "type": "string",
                            "required": True,
                            "default": "18.300231990440125",
                            "description": "Latitude"
                        },
                        {
                            "name": "lon",
                            "in": "query",
                            "type": "string",
                            "required": True,
                            "default": "-64.8251590359234",
                            "description": "Longitude"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/definitions/SuccessResponse"
                            }
                        },
                        "400": {
                            "description": "Bad Request",
                            "schema": {
                                "$ref": "#/definitions/StatusResponse"
                            }
                        },
                        "500": {
                            "description": "Internal Server Error",
                            "schema": {
                                "$ref": "#/definitions/StatusResponse"
                            }
                        }
                    }
                }
            },
            "/forecast": {
                "get": {
                    "summary": "Get Forecast",
                    "description": "Returns forecast for given coordinates OR city",
                    "tags": ["weather"],
                    "produces": ["application/json"],
                    "parameters": [
                        {
                            "name": "city",
                            "in": "query",
                            "type": "string",
                            "required": False,
                            "enum": [
                                "minsk",
                                "london",
                                "tokyo",
                                "shanghai",
                                "warsaw"
                            ],
                            "description": "City name (optional)"
                        },
                        {
                            "name": "lat",
                            "in": "query",
                            "type": "string",
                            "required": False,
                            "default": "53.9006",
                            "description": "Latitude (required if city not provided)"
                        },
                        {
                            "name": "lon",
                            "in": "query",
                            "type": "string",
                            "required": False,
                            "default": "27.5590",
                            "description": "Longitude (required if city not provided)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/definitions/SuccessResponse"
                            }
                        },
                        "400": {
                            "description": "Bad Request",
                            "schema": {
                                "$ref": "#/definitions/StatusResponse"
                            }
                        },
                        "500": {
                            "description": "Internal Server Error",
                            "schema": {
                                "$ref": "#/definitions/StatusResponse"
                            }
                        }
                    }
                }
            }
        },
        "definitions": {
            "StatusResponse": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"}
                }
            },
            "SuccessResponse": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"},
                    "data": {
                        "$ref": "#/definitions/CurrentWeather"
                    }
                }
            },
            "CurrentWeather": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"}
                }
            }
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
