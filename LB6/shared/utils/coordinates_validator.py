from decimal import Decimal


def validate_lat_lon(lat: Decimal, lon: Decimal) -> str | None:
    if not (-90 <= lat <= 90):
        return "invalid latitude"
    if not (-180 <= lon <= 180):
        return "invalid longitude"
    return None