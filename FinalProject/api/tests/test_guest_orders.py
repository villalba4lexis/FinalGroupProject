from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)


def generate_unique_name(prefix="Guest Club"):
    return f"{prefix} {uuid.uuid4()}"


def create_test_sandwich(name=None):
    name = name or generate_unique_name()
    response = client.post("/sandwiches/", json={
        "sandwich_name": name,
        "calories": 520,
        "price": 9.99,
        "category": "Guest"
    })
    assert response.status_code == 201
    return response.json()["id"]


def test_create_guest_order():
    sandwich_id = create_test_sandwich()
    response = client.post("/orders/guest-orders", json={
        "customer_name": "Alex Guest",
        "customer_phone": "555-111-2222",
        "customer_address": "123 Guest St.",
        "customer_email": "guest@example.com",
        "description": "No mayo, please.",
        "items": [
            {
                "sandwich_id": sandwich_id,
                "quantity": 2
            }
        ]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Alex Guest"
    assert data["status"] == "Pending"
    assert "tracking_number" in data


def test_guest_order_with_multiple_sandwiches():
    sandwich1 = create_test_sandwich("Multi A " + str(uuid.uuid4()))
    sandwich2 = create_test_sandwich("Multi B " + str(uuid.uuid4()))

    response = client.post("/orders/guest-orders", json={
        "customer_name": "Multi Sandwich Guest",
        "customer_phone": "555-222-3333",
        "customer_address": "456 Guest Blvd.",
        "customer_email": "multi@example.com",
        "description": "Two kinds please.",
        "items": [
            {"sandwich_id": sandwich1, "quantity": 1},
            {"sandwich_id": sandwich2, "quantity": 3}
        ]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Multi Sandwich Guest"
    assert len(data["order_details"]) == 2


def test_guest_order_tracking_retrieval():
    sandwich_id = create_test_sandwich()
    response = client.post("/orders/guest-orders", json={
        "customer_name": "Tracking Guest",
        "customer_phone": "555-444-5555",
        "customer_address": "789 Guest Way",
        "customer_email": "trackme@example.com",
        "description": "Check my status",
        "items": [
            {"sandwich_id": sandwich_id, "quantity": 1}
        ]
    })
    assert response.status_code == 201
    tracking_number = response.json()["tracking_number"]

    status_response = client.get(f"/orders/tracking/{tracking_number}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "Pending"


def test_guest_order_invalid_quantity():
    sandwich_id = create_test_sandwich()
    response = client.post("/orders/guest-orders", json={
        "customer_name": "Invalid Quantity",
        "customer_phone": "555-666-7777",
        "customer_address": "000 Invalid St",
        "customer_email": "invalid@example.com",
        "description": "This should fail",
        "items": [
            {"sandwich_id": sandwich_id, "quantity": -1}
        ]
    })
    assert response.status_code == 422


def test_guest_order_missing_fields():
    response = client.post("/orders/guest-orders", json={
        "customer_name": "Missing Fields",
        # Missing phone, address, and items
        "customer_email": "missing@example.com",
        "description": "This should also fail"
    })
    assert response.status_code == 422
