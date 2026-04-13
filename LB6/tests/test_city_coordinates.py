from decimal import Decimal

from LB6.shared.utils.city_coordinates import CityCoordinates


def test_resolve_known_city_english():
    lat, lon, err = CityCoordinates.resolve("London")

    assert err is None


def test_resolve_unknown_city():
    lat, lon, err = CityCoordinates.resolve("Berlin")

    assert err is not None
    assert "not supported" in str(err)
