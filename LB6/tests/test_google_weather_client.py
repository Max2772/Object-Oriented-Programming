from decimal import Decimal
from unittest.mock import patch

import pytest

from LB6.clients.google_weather import GoogleWeatherClient
from LB6.controllers.weather import WeatherController
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather


@pytest.fixture
def googleweather_client():
    return GoogleWeatherClient("test-key", "https://googleweather.com")


@pytest.fixture
def controller(googleweather_client):
    return WeatherController(googleweather_client)


@patch('requests.get')
def test_get_current_weather_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'temperature': {'degrees': 25.5}}

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
def test_get_forecast_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'forecastDays': [
        {'maxTemperature': {'degrees': 20}},
        {'maxTemperature': {'degrees': 22}},
        {'maxTemperature': {'degrees': 19}}
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


@patch('requests.get')
def test_get_current_weathers_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'temperature': {'degrees': 25.5}}

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_multiple_weather(locations)

    assert err is None
    assert len(result) == 2
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_weathers_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_multiple_weather(locations)

    assert err is not None
    assert len(result) == 0
    assert all(isinstance(r, Weather) for r in result)
