from typing import List
from app.models.schemas import DeliveryRequest, RouteStep, DeliveryResponse
from app.strategies.base_strategy import DeliveryOptimizerStrategy
from app.utils.geo import haversine_distance_km, calculate_travel_time


class EarliestFinishTimeOptimizer(DeliveryOptimizerStrategy):
    def __init__(self, speed_kmph: float = 20):
        self.speed_kmph = speed_kmph

    def optimize(self, request: DeliveryRequest) -> DeliveryResponse:
        orders = request.orders
        current_location = request.delivery_start_location
        delivery_steps: List[RouteStep] = []
        total_time = 0.0

        while orders:
            best_order = None
            best_total_time = float("inf")
            best_step_pair = None

            for order in orders:
                dist_to_rest = haversine_distance_km(
                    current_location, order.restaurant.location
                )
                travel_time_to_rest = calculate_travel_time(
                    dist_to_rest, self.speed_kmph
                )
                arrival_time_at_rest = total_time + travel_time_to_rest

                wait_time = max(0, order.prep_time - arrival_time_at_rest)

                dist_to_cust = haversine_distance_km(
                    order.restaurant.location, order.customer.location
                )
                travel_time_to_cust = calculate_travel_time(dist_to_cust)

                total_order_time = (
                    travel_time_to_rest + wait_time + travel_time_to_cust
                )  # noqa : E501

                if total_order_time < best_total_time:
                    best_total_time = total_order_time
                    best_order = order
                    best_step_pair = [
                        RouteStep(
                            action="pickup",
                            location=order.restaurant.location,
                            restaurant_name=order.restaurant.name,
                            travel_time_minutes=round(travel_time_to_rest, 2),
                            wait_time_minutes=round(wait_time, 2),
                        ),
                        RouteStep(
                            action="deliver",
                            location=order.customer.location,
                            customer_name=order.customer.name,
                            travel_time_minutes=round(travel_time_to_cust, 2),
                        ),
                    ]
            current_location = best_order.customer.location
            total_time += best_total_time

            delivery_steps.extend(best_step_pair)
            orders.remove(best_order)

        return DeliveryResponse(
            total_delivery_time_minutes=round(total_time, 2),
            detailed_steps=delivery_steps,
        )
