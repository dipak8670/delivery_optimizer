# 🚚 Delivery Optimizer API

A Python-based delivery optimization system built using **FastAPI** that computes the most efficient route to deliver food from multiple restaurants to multiple customers, minimizing total delivery time. The optimizer supports multiple strategies like **Earliest Finish Time (EFT)** and **TSP-based Optimization** via the **Strategy Design Pattern**.

---

## 🔧 Features

- Optimizes delivery order to minimize total delivery time.
- Accounts for:
  - Geolocation distance using the **Haversine formula**.
  - Food preparation time.
  - Travel and wait time.
- Pluggable strategy system using the **Strategy Design Pattern**.
- Easily extendable for more strategies.

---

## 🧱 Project Structure

```
delivery_optimizer/
├── app
|   ├── main.py                     # FastAPI app entry point
|   ├── api/
|   |   └── routes.py                   # API route definitions
|   ├── strategies/
|   │   ├── base_strategy.py             # Strategy pattern base class
|   │   ├── eft_optimizer.py         # Earliest Finish Time strategy
|   │   └── tsp_optimizer.py         # TSP-based optimization strategy
|   ├── models/
|   │   └── schema.py               # Pydantic models for API
|   ├──utils/
|   │   └── geo.py                  # Haversine and travel time utilities
|   ├──services/
|   │   └── delivery_service.py                  # Strategy selector based on request
├── tests/
|  └── test_delivery_optimizer.py       # Unit tests for strategies
├── Dockerfile                       # Dockerfile
├── Makefile                         # Contains commonly used make commands
└── requirements.txt                # Contains list of dependencies

```

---

## 🚀 API Endpoints

### 1. `POST /optimize`

Optimize delivery routes using selected strategy.

#### 🔸 Query Parameters:
- `strategy`: `eft` or `tsp` (default: `eft`)

#### 🔸 Request Body (JSON)

```json
{
  "delivery_start_location": {
    "latitude": 12.9611,
    "longitude": 77.5
  },
  "orders": [
    {
      "restaurant": {
        "name": "R1",
        "location": { "latitude": 12.9716, "longitude": 77.5946 }
      },
      "customer": {
        "name": "C1",
        "location": { "latitude": 12.9352, "longitude": 77.6146 }
      },
      "prep_time": 50
    },
    {
      "restaurant": {
        "name": "R2",
        "location": { "latitude": 12.9611, "longitude": 77.6387 }
      },
      "customer": {
        "name": "C2",
        "location": { "latitude": 12.9516, "longitude": 77.5846 }
      },
      "prep_time": 2
    }
  ]
}

```

#### 🔸 Sample Response

```json
{
    "total_delivery_time_minutes": 84.15,
    "detailed_steps": [
        {
            "action": "pickup",
            "location": {
                "latitude": 12.9611,
                "longitude": 77.6387
            },
            "restaurant_name": "R2",
            "customer_name": null,
            "travel_time_minutes": 45.09,
            "wait_time_minutes": 0.0
        },
        {
            "action": "deliver",
            "location": {
                "latitude": 12.9516,
                "longitude": 77.5846
            },
            "restaurant_name": null,
            "customer_name": "C2",
            "travel_time_minutes": 17.87,
            "wait_time_minutes": null
        },
        {
            "action": "pickup",
            "location": {
                "latitude": 12.9716,
                "longitude": 77.5946
            },
            "restaurant_name": "R1",
            "customer_name": null,
            "travel_time_minutes": 7.42,
            "wait_time_minutes": 0.0
        },
        {
            "action": "deliver",
            "location": {
                "latitude": 12.9352,
                "longitude": 77.6146
            },
            "restaurant_name": null,
            "customer_name": "C1",
            "travel_time_minutes": 13.77,
            "wait_time_minutes": null
        }
    ]
}
```

---

## 🧠 Strategies Implemented

### 🟩 1. **Earliest Finish Time (EFT)**
- Greedy strategy.
- At each step, picks the order with the lowest `travel + wait + delivery` time.

### 🟦 2. **TSP-Based Strategy**
- Considers all permutations of pickup/drop pairs.
- Selects the one with the lowest **total delivery time**.
- Best for small number of orders, else expensive.

---

## 🧩 Design Pattern: Strategy Pattern

Used to easily switch between different delivery optimization algorithms.

### Interface:
```python
class DeliveryOptimizerStrategy:
    def optimize(self, request: DeliveryRequest) -> DeliveryResponse:
        pass
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## ▶️ Running the App

```bash
make run    # Run the FastAPI app using Uvicorn
```

```bash
make dev    #Run app in auto-reload dev mode
```

Then open the docs at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 Python Version

Ensure you're using **Python 3.9+**
