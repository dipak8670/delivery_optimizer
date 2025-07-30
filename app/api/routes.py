from app.models.schemas import DeliveryRequest, DeliveryResponse
from app.services.delivery_service import DeliveryOptimizer
from fastapi import APIRouter

router = APIRouter()


@router.post("/optimize-delivery", response_model=DeliveryResponse)
def optimize_delivery(delivery_request: DeliveryRequest):
    optimizer = DeliveryOptimizer(speed_kmph=20)
    return optimizer.optimize_route(request=delivery_request)
