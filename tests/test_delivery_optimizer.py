import pytest
from app.models.schemas import (
    DeliveryRequest,
    Order,
    Location,
    RouteStep,
    DeliveryResponse,
    Restaurant,
    Customer,
)
from app.services.delivery_service import DeliveryOptimizer

optimizer = DeliveryOptimizer()


@pytest.fixture
def valid_location():
    return Location(latitude=12.9611, longitude=77.6387)


@pytest.fixture
def sample_request(valid_location, sample_orders):
    return DeliveryRequest(delivery_start_location=valid_location, orders=sample_orders)


@pytest.fixture
def sample_request():
    return DeliveryRequest(
        delivery_start_location=Location(latitude=12.9611, longitude=77.6387),
        orders=[
            Order(
                restaurant=Restaurant(
                    name="R1", location=Location(latitude=12.9616, longitude=77.6389)
                ),
                customer=Customer(
                    name="C1",
                    location=Location(latitude=12.9645, longitude=77.6400),
                ),
                prep_time=10,
            ),
            Order(
                restaurant=Restaurant(
                    name="R2", location=Location(latitude=12.9600, longitude=77.6390)
                ),
                customer=Customer(
                    name="C2", location=Location(latitude=12.9590, longitude=77.6375)
                ),
                prep_time=5,
            ),
        ],
    )


def test_delivery_response_structure(sample_request):
    response = optimizer.optimize_route(sample_request)
    assert isinstance(response, DeliveryResponse)
    assert isinstance(response.total_delivery_time_minutes, float)
    assert isinstance(response.detailed_steps, list)
    assert all(isinstance(step, RouteStep) for step in response.detailed_steps)


def test_step_fields_presence(sample_request):
    response = optimizer.optimize_route(sample_request)
    for step in response.detailed_steps:
        assert step.action in ("pickup", "deliver")
        assert isinstance(step.location.latitude, float)
        assert isinstance(step.location.longitude, float)
        assert isinstance(step.travel_time_minutes, float)
        if step.action == "pickup":
            assert step.restaurant_name is not None
            assert step.wait_time_minutes is not None
        if step.action == "deliver":
            assert step.customer_name is not None


def test_empty_orders():
    request = DeliveryRequest(
        delivery_start_location=Location(latitude=12.9611, longitude=77.6387), orders=[]
    )
    response = optimizer.optimize_route(request)
    assert isinstance(response, DeliveryResponse)
    assert response.total_delivery_time_minutes == 0
    assert response.detailed_steps == []


def test_invalid_location_coordinates():
    with pytest.raises(ValueError):
        _ = Location(latitude=999, longitude=77.0)

    with pytest.raises(ValueError):
        _ = Location(latitude=12.0, longitude=200)


def test_same_pickup_and_delivery_location(valid_location):
    location = Location(latitude=12.9611, longitude=77.6387)
    order = Order(
        restaurant=Restaurant(name="R1", location=location),
        customer=Customer(name="C1", location=location),
        prep_time=2,
    )
    request = DeliveryRequest(delivery_start_location=valid_location, orders=[order])
    response = optimizer.optimize_route(request)
    assert response.total_delivery_time_minutes >= 2
    assert any(step.travel_time_minutes == 0 for step in response.detailed_steps)
