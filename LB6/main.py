from dotenv import load_dotenv
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from LB6.shared.swagger.parameters import PROVIDER_PARAM, CITY_PARAM, LAT_PARAM, LON_PARAM
from LB6.shared.utils.city_coordinates import CityCoordinates
from api.weather import WeatherHandler

load_dotenv()

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = "/swagger"
API_URL = "/swagger.json"
API_PREFIX = "/api/v1"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Weather Example API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

weather_handler = WeatherHandler()


@app.route(f"{API_PREFIX}/weather", methods=["GET"])
def get_current_weather():
    return weather_handler.handler_get_current_weather()


@app.route(f"{API_PREFIX}/weather/multiple", methods=["GET"])
def get_multiple_current_weather():
    return weather_handler.handler_get_multiple_current_weather()


@app.route(f"{API_PREFIX}/forecast", methods=["GET"])
def get_forecast():
    return weather_handler.handler_get_forecast()


@app.route(f"{API_PREFIX}/cities", methods=["GET"])
def get_all_cities():
    return weather_handler.handler_get_all_cities()


@app.route("/swagger.json")
def swagger():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Weather Example API",
            "version": "1.0",
            "description": "Weather API for LB6 (OOP)"
        },
        "basePath": f"{API_PREFIX}",
        "paths": {
            "/weather": {
                "get": {
                    "summary": "Get Current Weather",
                    "description": "Returns current weather for given coordinates or city",
                    "tags": ["weather"],
                    "produces": ["application/json"],
                    "parameters": [
                        PROVIDER_PARAM,
                        CITY_PARAM,
                        LAT_PARAM,
                        LON_PARAM,
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
            "/weather/multiple": {
                "get": {
                    "summary": "Get Current Weather for Multiple Locations",
                    "description": "Returns current weather for multiple coordinates. Pass coordinates as comma-separated values: lat1,lon1,lat2,lon2,...",
                    "tags": ["weather"],
                    "produces": ["application/json"],
                    "parameters": [
                        PROVIDER_PARAM,
                        {
                            "name": "cords",
                            "in": "query",
                            "type": "string",
                            "required": True,
                            "default": "53.9,27.56,51.5074,-0.1278",
                            "description": "Comma-separated coordinates: lat1,lon1,lat2,lon2,... (must be even number of values)"
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
                        PROVIDER_PARAM,
                        CITY_PARAM,
                        LAT_PARAM,
                        LON_PARAM,
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
            "/cities": {
                "get": {
                    "summary": "Get All Cities",
                    "description": "Returns list of supported cities",
                    "tags": ["info"],
                    "produces": ["application/json"],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/definitions/SuccessResponse"
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
                        "type": "object"
                    }
                }
            },
            "Weather": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"}
                }
            },
            "Forecast": {
                "type": "object",
                "properties": {
                    "daily_max_temps": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8080
    )
