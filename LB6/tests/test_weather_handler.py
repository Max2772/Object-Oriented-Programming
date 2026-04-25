import os
from decimal import Decimal
from unittest.mock import patch

import pytest
from flask import Flask

from LB6.api.weather import WeatherHandler
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather

os.environ.setdefault("OPENWEATHER_API_KEY", "test-key")
os.environ.setdefault("OPENWEATHER_BASE_URL", "http://openweather.test")
os.environ.setdefault("GOOGLE_WEATHER_API_KEY", "test-key")
os.environ.setdefault("GOOGLE_BASE_URL", "http://google.test")


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    handler = WeatherHandler()
    app.add_url_rule("/weather", view_func=handler.handler_get_current_weather, methods=["GET"])
    app.add_url_rule("/forecast", view_func=handler.handler_get_forecast, methods=["GET"])
    app.add_url_rule("/weather/multiple", view_func=handler.handler_get_multiple_current_weather, methods=["GET"])
    app.add_url_rule("/cities", view_func=handler.handler_get_all_cities, methods=["GET"])
    return app.test_client()


def test_missing_provider_returns_400(client):
    resp = client.get("/weather?lat=53.9&lon=27.5")
    assert resp.status_code == 400


def test_invalid_provider_returns_400(client):
    resp = client.get("/weather?provider=unknown&lat=53.9&lon=27.5")
    assert resp.status_code == 400
    assert "invalid provider" in resp.get_json()["message"]


def test_missing_coordinates_returns_400(client):
    resp = client.get("/weather?provider=openweather")
    assert resp.status_code == 400


def test_non_numeric_coordinates_returns_400(client):
    resp = client.get("/weather?provider=openweather&lat=abc&lon=27.5")
    assert resp.status_code == 400
    assert "invalid coordinates" in resp.get_json()["message"]


def test_out_of_range_latitude_returns_400(client):
    resp = client.get("/weather?provider=openweather&lat=999&lon=27.5")
    assert resp.status_code == 400
    assert "invalid latitude" in resp.get_json()["message"]


def test_out_of_range_longitude_returns_400(client):
    resp = client.get("/weather?provider=openweather&lat=53.9&lon=999")
    assert resp.status_code == 400
    assert "invalid longitude" in resp.get_json()["message"]


def test_city_and_lat_together_returns_400(client):
    resp = client.get("/weather?provider=openweather&city=minsk&lat=53.9")
    assert resp.status_code == 400
    assert "too many arguments" in resp.get_json()["message"]


def test_unknown_city_returns_400(client):
    resp = client.get("/weather?provider=openweather&city=atlantis")
    assert resp.status_code == 400


def test_success_with_coords_openweather(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_current_weather.return_value = (Weather(Decimal("12.5")), None)
        resp = client.get("/weather?provider=openweather&lat=53.9&lon=27.5")
    assert resp.status_code == 200
    assert resp.get_json()["data"]["temperature"] == 12.5


def test_success_with_coords_googleweather(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_current_weather.return_value = (Weather(Decimal("20.0")), None)
        resp = client.get("/weather?provider=googleweather&lat=35.68&lon=139.69")
    assert resp.status_code == 200
    assert resp.get_json()["data"]["temperature"] == 20.0


def test_success_with_city_name(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_current_weather.return_value = (Weather(Decimal("5.0")), None)
        resp = client.get("/weather?provider=openweather&city=minsk")
    assert resp.status_code == 200


def test_client_error_returns_400(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_current_weather.return_value = (
            Weather(Decimal("0")), Exception("API down")
        )
        resp = client.get("/weather?provider=openweather&lat=53.9&lon=27.5")
    assert resp.status_code == 400
    assert "API down" in resp.get_json()["message"]


def test_forecast_success(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_forecast.return_value = (
            Forecast([Decimal("10"), Decimal("12"), Decimal("9")]), None
        )
        resp = client.get("/forecast?provider=openweather&lat=53.9&lon=27.5")
    assert resp.status_code == 200
    assert resp.get_json()["data"]["daily_max_temps"] == [10.0, 12.0, 9.0]


def test_forecast_missing_provider_returns_400(client):
    resp = client.get("/forecast?lat=53.9&lon=27.5")
    assert resp.status_code == 400


def test_forecast_client_error_returns_400(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_forecast.return_value = (
            Forecast([]), Exception("forecast unavailable")
        )
        resp = client.get("/forecast?provider=openweather&lat=53.9&lon=27.5")
    assert resp.status_code == 400


def test_forecast_with_city(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_forecast.return_value = (
            Forecast([Decimal("7"), Decimal("8")]), None
        )
        resp = client.get("/forecast?provider=openweather&city=tokyo")
    assert resp.status_code == 200


def test_multiple_by_cities(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_multiple_weather.return_value = (
            [Weather(Decimal("5")), Weather(Decimal("15"))], None
        )
        resp = client.get("/weather/multiple?provider=openweather&cities=minsk,london")
    assert resp.status_code == 200
    assert len(resp.get_json()["data"]) == 2


def test_multiple_by_raw_coords(client):
    with patch("LB6.api.weather.WeatherController") as mock_ctrl:
        mock_ctrl.return_value.get_multiple_weather.return_value = (
            [Weather(Decimal("8")), Weather(Decimal("18"))], None
        )
        resp = client.get("/weather/multiple?provider=openweather&coords=53.9,27.5,51.5,-0.1")
    assert resp.status_code == 200
    assert len(resp.get_json()["data"]) == 2


def test_multiple_odd_coords_returns_400(client):
    resp = client.get("/weather/multiple?provider=openweather&coords=53.9,27.5,51.5")
    assert resp.status_code == 400
    assert "even amount" in resp.get_json()["message"]


def test_multiple_cities_and_coords_together_returns_400(client):
    resp = client.get("/weather/multiple?provider=openweather&cities=minsk&coords=53.9,27.5")
    assert resp.status_code == 400
    assert "too many arguments" in resp.get_json()["message"]


def test_multiple_unknown_city_returns_400(client):
    resp = client.get("/weather/multiple?provider=openweather&cities=minsk,varsaw")
    assert resp.status_code == 400
    assert "invalid city" in resp.get_json()["message"]


def test_multiple_no_locations_returns_400(client):
    resp = client.get("/weather/multiple?provider=openweather")
    assert resp.status_code == 400


def test_multiple_invalid_coords_returns_400(client):
    resp = client.get("/weather/multiple?provider=openweather&coords=abc,27.5")
    assert resp.status_code == 400


def test_get_cities_returns_200(client):
    resp = client.get("/cities")
    assert resp.status_code == 200


def test_get_cities_contains_all_five(client):
    resp = client.get("/cities")
    data = resp.get_json()["data"]
    for city in ("minsk", "london", "tokyo", "shanghai", "warsaw"):
        assert city in data
