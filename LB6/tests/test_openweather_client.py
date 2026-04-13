from decimal import Decimal
from unittest.mock import Mock

from LB6.controllers.weather import CurrentWeatherController
from LB6.models.weather.get import Weather
from LB6.models.forecast.get import Forecast


def test_get_current_weather_success():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('25.5'), None)
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Weather)
    assert result.temperature == Decimal('25.5')


def test_get_current_weather_api_error():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('0'), Exception("Weather API error"))
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "Weather API error" in str(err)
    assert result.temperature == Decimal('0')


def test_get_forecast_success():
    mock_client = Mock()
    mock_forecast = Forecast([Decimal('20'), Decimal('22'), Decimal('19')])
    mock_client.get_forecast.return_value = (mock_forecast, None)
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, Forecast)
    assert result.daily_max_temps == [Decimal('20'), Decimal('22'), Decimal('19')]


def test_get_forecast_error():
    mock_client = Mock()
    mock_client.get_forecast.return_value = (Forecast([]), Exception("Forecast API error"))
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_forecast(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "Forecast API error" in str(err)
