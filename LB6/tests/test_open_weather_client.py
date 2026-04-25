from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
import requests

from LB6.clients.open_weather import OpenWeatherClient
from LB6.controllers.weather import WeatherController
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather
from LB6.shared.utils.city_coordinates import CityCoordinates


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
def test_get_current_weather_server_error_500(mock_get, controller):
    mock_get.return_value.status_code = 500

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "bad status" in str(err)
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_current_weather_network_error(mock_get, controller):
    mock_get.side_effect = requests.RequestException("timeout")

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_current_weather_missing_main_key(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_current_weather_missing_temp_key(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {}}

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_current_weather_negative_temperature(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': -15.3}}

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert result.temperature == Decimal('-15.3')


@patch('requests.get')
def test_get_current_weather_zero_temperature(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 0}}

    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert result.temperature == Decimal('0')


@patch('requests.get')
def test_get_forecast_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': [
        {'main': {'temp': 20}},
        {'main': {'temp': 22}},
        {'main': {'temp': 19}},
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
def test_get_forecast_network_error(mock_get, controller):
    mock_get.side_effect = requests.RequestException("timeout")

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert isinstance(result, Forecast)
    assert result.daily_max_temps == []


@patch('requests.get')
def test_get_forecast_empty_list(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': []}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert result.daily_max_temps == []


@patch('requests.get')
def test_get_forecast_missing_list_key(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert result.daily_max_temps == []


@patch('requests.get')
def test_get_forecast_skips_items_without_temp(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': [
        {'main': {'temp': 20}},
        {'main': {}},
        {'main': {'temp': 19}},
    ]}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "bad data" in str(err)
    assert result.daily_max_temps == []


@patch('requests.get')
def test_get_forecast_applies_step_for_40_plus_items(mock_get, controller):
    items = [{'main': {'temp': float(i)}} for i in range(40)]
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': items}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    expected = [Decimal(str(float(i))) for i in range(0, 40, 8)]
    assert result.daily_max_temps == expected


@patch('requests.get')
def test_get_forecast_no_step_for_less_than_40_items(mock_get, controller):
    items = [{'main': {'temp': float(i)}} for i in range(10)]
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'list': items}

    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert len(result.daily_max_temps) == 10


@patch('requests.get')
def test_get_current_weathers_coords_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 25.5}}

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_multiple_weather(locations)

    assert err is None
    assert len(result) == 2
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_weathers_coords_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_multiple_weather(locations)

    assert err is not None
    assert len(result) == 0
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_weathers_empty_locations(mock_get, controller):
    result, err = controller.get_multiple_weather([])

    assert err is None
    assert result == []
    mock_get.assert_not_called()


@patch('requests.get')
def test_get_current_weathers_single_location(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 10.0}}

    result, err = controller.get_multiple_weather([(Decimal('35.68'), Decimal('139.69'))])

    assert err is None
    assert len(result) == 1
    assert result[0].temperature == Decimal('10.0')


@patch('requests.get')
def test_get_current_weathers_stops_on_first_error(mock_get, controller):
    success = MagicMock()
    success.status_code = 200
    success.json.return_value = {'main': {'temp': 20.0}}

    failure = MagicMock()
    failure.status_code = 500

    mock_get.side_effect = [success, failure]

    locations = [
        (Decimal('53.9'), Decimal('27.56')),
        (Decimal('51.5'), Decimal('-0.12')),
    ]
    result, err = controller.get_multiple_weather(locations)

    assert err is not None
    assert result == []


@patch('requests.get')
def test_get_current_weathers_cities_success(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 25.5}}

    cities = ["minsk", "london"]
    locations = []
    for city in cities:
        lat, lon, err = CityCoordinates.resolve(city)
        assert err is None
        locations.append((lat, lon))

    result, err = controller.get_multiple_weather(locations)

    assert err is None
    assert len(result) == 2
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_weathers_cities_error(mock_get, controller):
    mock_get.return_value.status_code = 401

    cities = ["minsk", "london"]
    locations = []
    for city in cities:
        lat, lon, err = CityCoordinates.resolve(city)
        assert err is None
        locations.append((lat, lon))

    result, err = controller.get_multiple_weather(locations)

    assert err is not None
    assert len(result) == 0
    assert all(isinstance(r, Weather) for r in result)


@patch('requests.get')
def test_get_current_weathers_all_five_cities(mock_get, controller):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'main': {'temp': 15.0}}

    cities = ["minsk", "london", "tokyo", "shanghai", "warsaw"]
    locations = []
    for city in cities:
        lat, lon, err = CityCoordinates.resolve(city)
        assert err is None
        locations.append((lat, lon))

    result, err = controller.get_multiple_weather(locations)

    assert err is None
    assert len(result) == 5
    assert all(isinstance(r, Weather) for r in result)
