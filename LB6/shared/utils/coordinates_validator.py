from decimal import Decimal


def valid_lat_lon(lat: Decimal, lon: Decimal) -> tuple[bool, str | None]:
    if not (-90 <= lat <= 90):
        return False,"invalid latitude"
    if not (-180 <= lon <= 180):
        return False, "invalid longitude"
    return True, None