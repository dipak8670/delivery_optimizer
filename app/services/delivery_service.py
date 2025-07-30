from typing import List
from app.models.schemas import DeliveryRequest, RouteStep, DeliveryResponse
from app.utils.geo import haversine_distance_km
from app.utils.time import calculate_travel_time


class DeliveryOptimizer:
    def __init__(self, speed_kmph: float = 20):
        self.speed_kmph = speed_kmph

    def optimize_route(self, request: DeliveryRequest) -> DeliveryResponse:
        route_steps: List[RouteStep] = []
        current_time = 0.0
        current_location = request.delivery_start_location

        picked_orders = set()

        orders_sorted = sorted(
            request.orders, key=lambda order: order.restaurant.prep_time
        )

        for order in orders_sorted:
            rest = order.restaurant
            dist = haversine_distance_km(current_location, rest.location)
            travel_time = calculate_travel_time(dist, self.speed_kmph)

            arrival_time = current_time + travel_time
            wait_time = max(0, rest.prep_time - arrival_time)

            route_steps.append(
                RouteStep(
                    action="pickup",
                    location=rest.location,
                    restaurant_name=rest.name,
                    travel_time_minutes=travel_time,
                    wait_time_minutes=wait_time,
                )
            )

            current_time += travel_time + wait_time
            current_location = rest.location
            picked_orders.add(order.customer.name)

        for order in orders_sorted:
            cust = order.customer
            dist = haversine_distance_km(current_location, cust.location)
            travel_time = calculate_travel_time(dist, self.speed_kmph)

            route_steps.append(
                RouteStep(
                    action="deliver",
                    location=cust.location,
                    customer_name=cust.name,
                    travel_time_minutes=travel_time,
                )
            )

            current_time += travel_time
            current_location = cust.location

        return DeliveryResponse(
            total_delivery_time_minutes=round(current_time, 2),
            detailed_steps=route_steps,
        )
