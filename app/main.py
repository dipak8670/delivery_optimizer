from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Delivery Optimizer",
    description="Optimizes delivery route based on restuarant prep time and geolocation",  # noqa: E501
    version="1.0.0",
)

app.include_router(router, prefix="/api")
