from itertools import permutations
from app.models.schemas import RouteStep, DeliveryRequest, DeliveryResponse
from app.strategies.base_strategy import DeliveryOptimizerStrategy
from app.utils.geo import haversine_distance_km, calculate_travel_time


class TspOptimizer(DeliveryOptimizerStrategy):
    def __init__(self, speed_kmph: float = 20):
        self.speed_kmph = speed_kmph

    def optimize(self, request: DeliveryRequest) -> DeliveryResponse:
        start_location = request.delivery_start_location
        orders = request.orders
        best_route = []
        min_total_time = float("inf")

        for perm in permutations(orders):
            current_location = start_location
            current_time = 0.0
            route_steps = []

            for order in perm:
                dist_to_rest = haversine_distance_km(
                    current_location, order.restaurant.location
                )  # noqa : E501
                travel_to_rest = calculate_travel_time(
                    dist_to_rest, self.speed_kmph
                )  # noqa : E501
                arrival_time = current_time + travel_to_rest

                wait_time = max(0.0, order.prep_time - arrival_time)

                route_steps.append(
                    RouteStep(
                        action="pickup",
                        location=order.restaurant.location,
                        restaurant_name=order.restaurant.name,
                        customer_name=None,
                        travel_time_minutes=round(travel_to_rest, 2),
                        wait_time_minutes=round(wait_time, 2),
                    )
                )

                current_time += travel_to_rest + wait_time
                current_location = order.restaurant.location

                dist_to_cust = haversine_distance_km(
                    current_location, order.customer.location
                )  # noqa : E501
                travel_to_cust = calculate_travel_time(
                    dist_to_cust, self.speed_kmph
                )  # noqa : E501

                route_steps.append(
                    RouteStep(
                        action="deliver",
                        location=order.customer.location,
                        restaurant_name=None,
                        customer_name=order.customer.name,
                        travel_time_minutes=round(travel_to_cust, 2),
                        wait_time_minutes=0.0,
                    )
                )

                current_time += travel_to_cust
                current_location = order.customer.location

            if current_time < min_total_time:
                min_total_time = current_time
                best_route = route_steps

        return DeliveryResponse(
            total_delivery_time_minutes=round(min_total_time, 2),
            detailed_steps=best_route,
        )
