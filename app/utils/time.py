def calculate_travel_time(
    distance_km: float, speed_kmph: float = 20.0
) -> float:  # noqa: E501
    return round((distance_km / speed_kmph) * 60, 2)
