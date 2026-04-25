from decimal import Decimal

from LB6.shared.utils.coordinates_validator import valid_lat_lon


def test_valid_typical_coordinates():
    valid, err = valid_lat_lon(Decimal('53.9'), Decimal('27.56'))
    assert valid is True
    assert err is None


def test_valid_zero_zero():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('0'))
    assert valid is True
    assert err is None


def test_valid_negative_latitude_and_longitude():
    valid, err = valid_lat_lon(Decimal('-33.8'), Decimal('-70.6'))
    assert valid is True
    assert err is None


def test_latitude_boundary_plus_90():
    valid, err = valid_lat_lon(Decimal('90'), Decimal('0'))
    assert valid is True
    assert err is None


def test_latitude_boundary_minus_90():
    valid, err = valid_lat_lon(Decimal('-90'), Decimal('0'))
    assert valid is True
    assert err is None


def test_latitude_just_above_90_is_invalid():
    valid, err = valid_lat_lon(Decimal('90.0001'), Decimal('0'))
    assert valid is False
    assert err is not None
    assert "latitude" in err.lower()


def test_latitude_just_below_minus_90_is_invalid():
    valid, err = valid_lat_lon(Decimal('-90.0001'), Decimal('0'))
    assert valid is False
    assert err is not None
    assert "latitude" in err.lower()


def test_latitude_far_out_of_range_is_invalid():
    valid, err = valid_lat_lon(Decimal('200'), Decimal('0'))
    assert valid is False
    assert err is not None
    assert "latitude" in err.lower()


def test_longitude_boundary_plus_180():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('180'))
    assert valid is True
    assert err is None


def test_longitude_boundary_minus_180():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('-180'))
    assert valid is True
    assert err is None


def test_longitude_just_above_180_is_invalid():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('180.0001'))
    assert valid is False
    assert err is not None
    assert "longitude" in err.lower()


def test_longitude_just_below_minus_180_is_invalid():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('-180.0001'))
    assert valid is False
    assert err is not None
    assert "longitude" in err.lower()


def test_longitude_far_out_of_range_is_invalid():
    valid, err = valid_lat_lon(Decimal('0'), Decimal('360'))
    assert valid is False
    assert err is not None
    assert "longitude" in err.lower()


def test_both_invalid_returns_latitude_error_first():
    valid, err = valid_lat_lon(Decimal('200'), Decimal('400'))
    assert valid is False
    assert err is not None
    assert "latitude" in err.lower()

def test_invalid_input_returns_false_and_string():
    valid, err = valid_lat_lon(Decimal('999'), Decimal('0'))
    assert valid is False
    assert isinstance(err, str)
    assert "latitude" in err.lower()
