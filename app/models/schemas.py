from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")


class Restaurant(BaseModel):
    name: str = Field(..., min_length=1, description="Restaurant Name")
    location: Location = Field(..., description="Location of the restaurant")


class Customer(BaseModel):
    name: str = Field(..., min_length=1, description="Customer Name")
    location: Location = Field(..., description="Location of the customer")


class Order(BaseModel):
    restaurant: Restaurant
    customer: Customer
    prep_time: float = Field(..., gt=0)


class DeliveryRequest(BaseModel):
    delivery_start_location: Location
    orders: List[Order]


class RouteStep(BaseModel):
    action: Literal["pickup", "deliver"]
    location: Location
    restaurant_name: Optional[str] = None
    customer_name: Optional[str] = None
    travel_time_minutes: float
    wait_time_minutes: Optional[float] = None


class DeliveryResponse(BaseModel):
    total_delivery_time_minutes: float
    detailed_steps: List[RouteStep]
