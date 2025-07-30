import math
from typing import Optional
from app.models.schemas import Location


def haversine_distance_km(loc1: Optional[Location], loc2: Optional[Location]):
    if loc1 is None or loc2 is None:
        return 0.0

    R = 6371.0

    lat1, lon1 = loc1.latitude, loc1.longitude
    lat2, lon2 = loc2.latitude, loc2.longitude

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
