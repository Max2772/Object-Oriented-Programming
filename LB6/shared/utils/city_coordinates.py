from decimal import Decimal
from typing import Tuple, Optional


class CityCoordinates:
    _CITIES = {
        "minsk": (Decimal("53.9006"), Decimal("27.5590")),
        "london": (Decimal("51.5074"), Decimal("-0.1278")),
        "tokyo": (Decimal("35.6895"), Decimal("139.6917")),
        "shanghai": (Decimal("31.2304"), Decimal("121.4737")),
        "warsaw": (Decimal("52.2297"), Decimal("21.0122")),
    }

    @classmethod
    def get_cities_list(cls) -> list[str]:
        return list(cls._CITIES.keys())

    @staticmethod
    def resolve(city: str) -> Tuple[Decimal, Decimal, Optional[Exception]]:
        city = city.strip().lower()
        if not city:
            return Decimal('0'), Decimal('0'), Exception("city is required")
        if city in CityCoordinates._CITIES:
            return CityCoordinates._CITIES[city][0], CityCoordinates._CITIES[city][1], None
        return Decimal('0'), Decimal('0'), Exception(
            f"City '{city}' not supported. Supported: {', '.join(CityCoordinates._CITIES.keys())}"
        )