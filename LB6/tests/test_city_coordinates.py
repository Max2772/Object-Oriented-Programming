from decimal import Decimal

from LB6.shared.utils.city_coordinates import CityCoordinates


def test_resolve_known_city_english():
    lat, lon, err = CityCoordinates.resolve("London")
    assert err is None
    assert isinstance(lat, Decimal)
    assert isinstance(lon, Decimal)


def test_resolve_unknown_city():
    lat, lon, err = CityCoordinates.resolve("Berlin")
    assert err is not None
    assert "not supported" in str(err)


def test_resolve_empty_city():
    lat, lon, err = CityCoordinates.resolve("")
    assert err is not None
    assert "city is required" in str(err)


def test_resolve_all_supported_cities():
    cities = ["minsk", "london", "tokyo", "shanghai", "warsaw"]
    for city in cities:
        lat, lon, err = CityCoordinates.resolve(city)
        assert err is None
        assert isinstance(lat, Decimal)
        assert isinstance(lon, Decimal)


def test_resolve_case_insensitive():
    lat, lon, err = CityCoordinates.resolve("LONdon")
    assert err is None
    assert isinstance(lat, Decimal)
    assert isinstance(lon, Decimal)