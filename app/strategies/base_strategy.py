from abc import ABC, abstractmethod
from app.models.schemas import DeliveryRequest, DeliveryResponse


class DeliveryOptimizerStrategy(ABC):
    @abstractmethod
    def optimize(self, request: DeliveryRequest) -> DeliveryResponse:
        pass
