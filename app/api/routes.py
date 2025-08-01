from app.models.schemas import DeliveryRequest, DeliveryResponse
from app.services.delivery_service import DeliveryService
from app.strategies.eft_optimizer import EarliestFinishTimeOptimizer
from fastapi import APIRouter, HTTPException, Query

from app.strategies.tsp_optimizer import TspOptimizer

router = APIRouter()


@router.post("/optimize", response_model=DeliveryResponse)
def optimize_delivery(
    request: DeliveryRequest, strategy: str = Query("eft", enum=["eft", "tsp"])
):
    if strategy == "eft":
        optimizer = EarliestFinishTimeOptimizer()
    elif strategy == "tsp":
        optimizer = TspOptimizer()
    else:
        raise HTTPException(status_code=400, detail="Invalid strategy")

    service = DeliveryService(optimizer)

    try:
        return service.get_optimized_route(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during optimization: {str(e)}"
        )
