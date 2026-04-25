from decimal import Decimal

import pytest

from LB6.shared.utils.city_coordinates import CityCoordinates

CITY_DATA = {
    "minsk": (Decimal("53.9006"), Decimal("27.5590")),
    "london": (Decimal("51.5074"), Decimal("-0.1278")),
    "tokyo": (Decimal("35.6895"), Decimal("139.6917")),
    "shanghai": (Decimal("31.2304"), Decimal("121.4737")),
    "warsaw": (Decimal("52.2297"), Decimal("21.0122")),
}

SUPPORTED_CITIES = list(CITY_DATA.keys())


def test_resolve_known_city():
    lat, lon, err = CityCoordinates.resolve("London")
    assert err is None
    assert isinstance(lat, Decimal)
    assert isinstance(lon, Decimal)


def test_resolve_all_supported_cities():
    for city in SUPPORTED_CITIES:
        lat, lon, err = CityCoordinates.resolve(city)
        assert err is None, f"Expected no error for city '{city}', got: {err}"
        assert isinstance(lat, Decimal)
        assert isinstance(lon, Decimal)


def test_resolve_case_insensitive():
    lat, lon, err = CityCoordinates.resolve("LONdon")
    assert err is None
    assert isinstance(lat, Decimal)
    assert isinstance(lon, Decimal)


def test_resolve_city_with_leading_trailing_whitespace():
    lat, lon, err = CityCoordinates.resolve("  minsk  ")
    assert err is None
    assert isinstance(lat, Decimal)
    assert isinstance(lon, Decimal)


@pytest.mark.parametrize(
    "city,expected_lat,expected_lon",
    [(city, lat, lon) for city, (lat, lon) in CITY_DATA.items()]
)
def test_resolve_exact_coordinates(city, expected_lat, expected_lon):
    lat, lon, err = CityCoordinates.resolve(city)
    assert err is None
    assert lat == expected_lat
    assert lon == expected_lon


def test_resolve_unknown_city():
    lat, lon, err = CityCoordinates.resolve("Berlin")
    assert err is not None
    assert "not supported" in str(err)


def test_resolve_empty_city():
    lat, lon, err = CityCoordinates.resolve("")
    assert err is not None
    assert "city is required" in str(err)


def test_resolve_whitespace_only_city():
    lat, lon, err = CityCoordinates.resolve("   ")
    assert err is not None
    assert "city is required" in str(err)


def test_resolve_unknown_city_returns_zero_coordinates():
    lat, lon, err = CityCoordinates.resolve("Atlantis")
    assert err is not None
    assert lat == Decimal('0')
    assert lon == Decimal('0')


def test_resolve_empty_city_returns_zero_coordinates():
    lat, lon, err = CityCoordinates.resolve("")
    assert err is not None
    assert lat == Decimal('0')
    assert lon == Decimal('0')


def test_resolve_unknown_city_error_message_lists_supported():
    _, _, err = CityCoordinates.resolve("Unknown")
    assert any(
        city in str(err).lower()
        for city in SUPPORTED_CITIES
    )


def test_get_cities_list_returns_list():
    cities = CityCoordinates.get_cities_list()
    assert isinstance(cities, list)


def test_get_cities_list_contains_all_five_cities():
    cities = CityCoordinates.get_cities_list()
    for expected in SUPPORTED_CITIES:
        assert expected in cities, f"Expected '{expected}' in cities list"


def test_get_cities_list_exact_count():
    cities = CityCoordinates.get_cities_list()
    assert len(cities) == len(SUPPORTED_CITIES)


def test_get_cities_list_all_lowercase():
    cities = CityCoordinates.get_cities_list()
    for city in cities:
        assert city == city.lower(), f"City '{city}' is not lowercase"
