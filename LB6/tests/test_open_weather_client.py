from decimal import Decimal
from unittest.mock import patch

import pytest

from LB6.clients.open_weather import OpenWeatherClient
from LB6.controllers.weather import WeatherController
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather


@pytest.fixture
def openweather_client():
    return OpenWeatherClient("test-key", "https://openweather.com")


@pytest.fixture
def controller(openweather_client):
    return WeatherController(openweather_client)


@patch('requests.get')
def test_get_current_weather_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 25.5}}

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Weather)
    assert result.temperature == Decimal('25.5')


@patch('requests.get')
def test_get_current_weather_api_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "bad status" in str(err)
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_current_temperatures_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 25.5}}

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_current_temperatures(locations)

    assert err is None
    assert len(result) == 2
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_temperatures_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_current_temperatures(locations)

    assert err is not None
    assert len(result) == 0
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_forecast_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': [
        {'main': {'temp': 20}},
        {'main': {'temp': 22}},
        {'main': {'temp': 19}}
    ]}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Forecast)
    assert result.daily_max_temps == [Decimal('20'), Decimal('22'), Decimal('19')]


@patch('requests.get')
def test_get_forecast_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "bad status" in str(err)
