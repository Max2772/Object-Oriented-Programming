from decimal import Decimal
from unittest.mock import Mock

from LB6.controllers.weather import CurrentWeatherController
from LB6.models.weather.get import CurrentWeather


def test_get_current_weather_success():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('25.5'), None)
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is None
    assert isinstance(result, CurrentWeather)
    assert result.temperature == Decimal('25.5')


def test_get_current_weather_api_error():
    mock_client = Mock()
    mock_client.location_current_temperature.return_value = (Decimal('0'), Exception("API error"))
    controller = CurrentWeatherController(mock_client)
    result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.56'))

    assert err is not None
    assert "API error" in str(err)
    assert result.temperature == Decimal('0')
