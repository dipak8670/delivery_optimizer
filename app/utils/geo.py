from math import radians, cos, sin, sqrt, atan2
from typing import Optional
from app.models.schemas import Location


def haversine_distance_km(loc1: Optional[Location], loc2: Optional[Location]):
    if loc1 is None or loc2 is None:
        return 0.0

    R = 6371.0

    lat1, lon1 = radians(loc1.latitude), radians(loc1.longitude)
    lat2, lon2 = radians(loc2.latitude), radians(loc2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def calculate_travel_time(
    distance_km: float, speed_kmph: float = 20.0
) -> float:  # noqa: E501
    return round((distance_km / speed_kmph) * 60, 2)
