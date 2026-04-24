from LB6.shared.swagger.parameters import PROVIDER_PARAM, CITY_PARAM, LAT_PARAM, LON_PARAM, CITIES_PARAM

PATHS = {
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
            "description": "Returns current weather for multiple coordinates. \nPass cities or coordinates as comma-separated values: city1, city2, city3... or lat1,lon1,lat2,lon2,...",
            "tags": ["weather"],
            "produces": ["application/json"],
            "parameters": [
                PROVIDER_PARAM,
                CITIES_PARAM,
                {
                    "name": "coords",
                    "in": "query",
                    "type": "string",
                    "required": False,
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
}
