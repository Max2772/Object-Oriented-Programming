from dotenv import load_dotenv
from flask import Flask

from LB6.shared.config import API_PREFIX, SWAGGER_URL
from LB6.shared.swagger.builder import build_swagger, swaggerui_blueprint
from LB6.api.weather import WeatherHandler

load_dotenv()

app = Flask(__name__)

# Swagger UI configuration
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
    return build_swagger()


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8080
    )
