from decimal import Decimal
from unittest.mock import Mock

from LB6.controllers.weather import WeatherController
from LB6.models.forecast.get import Forecast
from LB6.models.weather.get import Weather


def test_get_current_weather_success():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('25.5'), None)
    controller = WeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Weather)
    assert result.temperature == Decimal('25.5')


def test_get_current_weather_api_error():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('0'), Exception("Weather API error"))
    controller = WeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "Weather API error" in str(err)
    assert result.temperature == Decimal('0')


def test_get_current_temperatures_success():
    mock_client = Mock()
    mock_client.get_current_temperatures.return_value = ([Decimal('25.5'), Decimal('18.0')], None)
    controller = WeatherController(mock_client)
    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_current_temperatures(locations)

    assert err is None
    assert len(result) == 2
    assert all(isinstance(r, Weather) for r in result)


def test_get_current_temperatures_error():
    mock_client = Mock()
    mock_client.get_current_temperatures.return_value = ([Decimal('0'), Decimal('0')], Exception("Weather API error"))
    controller = WeatherController(mock_client)
    locations = [(Decimal('53.9'), Decimal('27.56')), (Decimal('51.5'), Decimal('-0.12'))]
    result, err = controller.get_current_temperatures(locations)

    assert err is not None
    assert len(result) == 0
    assert all(isinstance(r, Weather) for r in result)


def test_get_forecast_success():
    mock_client = Mock()
    mock_forecast = Forecast([Decimal('20'), Decimal('22'), Decimal('19')])
    mock_client.get_forecast.return_value = (mock_forecast, None)
    controller = WeatherController(mock_client)
    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Forecast)
    assert result.daily_max_temps == [Decimal('20'), Decimal('22'), Decimal('19')]


def test_get_forecast_error():
    mock_client = Mock()
    mock_client.get_forecast.return_value = (Forecast([]), Exception("Forecast API error"))
    controller = WeatherController(mock_client)
    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "Forecast API error" in str(err)
