from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Tuple, Optional, List

from LB6.models.forecast.get import Forecast


class WeatherDataClient(ABC):
    @abstractmethod
    def location_current_temperature(self, lat: Decimal, lon: Decimal) -> Tuple[Decimal, Optional[Exception]]:
        pass

    @abstractmethod
    def get_current_temperatures(self, locations: List[Tuple[Decimal, Decimal]]) -> Tuple[List[Decimal], Optional[Exception]]:
        pass

    @abstractmethod
    def get_forecast(self, lat: Decimal, lon: Decimal) -> Tuple[Forecast, Optional[Exception]]:
        pass
