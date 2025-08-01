from app.models.schemas import DeliveryRequest, DeliveryResponse
from app.strategies.base_strategy import DeliveryOptimizerStrategy


class DeliveryService:
    def __init__(self, strategy: DeliveryOptimizerStrategy):
        self.strategy = strategy

    def get_optimized_route(
        self, request: DeliveryRequest
    ) -> DeliveryResponse:  # noqa : E501
        return self.strategy.optimize(request)
