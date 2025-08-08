from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)


def generate_unique_name(base: str = "Trackable Sandwich") -> str:
    return f"{base} {uuid.uuid4()}"


class TestOrderTrackingFlow:

    def test_order_tracking_flow(self):
        sandwich_res = client.post("/sandwiches/", json={
            "sandwich_name": generate_unique_name(),
            "calories": 420,
            "price": 7.99,
            "category": "Dinner"
        })
        assert sandwich_res.status_code == 201
        sandwich_id = sandwich_res.json()["id"]

        order_res = client.post("/orders/guest-orders", json={
            "customer_name": "Tracking Tester",
            "customer_phone": "555-333-1111",
            "customer_address": "987 Nowhere Ln",
            "customer_email": "track@example.com",
            "description": "Track this order",
            "items": [
                {"sandwich_id": sandwich_id, "quantity": 1}
            ]
        })
        assert order_res.status_code == 201
        tracking_number = order_res.json()["tracking_number"]
        print("Tracking Number:", tracking_number)

        get_res = client.get(f"/orders/tracking/{tracking_number}")
        print("Initial Status Response:", get_res.json())
        assert get_res.status_code == 200
        assert get_res.json()["status"] == "Pending"

        update_res = client.put("/orders/tracking/update", json={
            "tracking_number": tracking_number,
            "status": "Delivered"
        })
        print("Updated Status Response:", update_res.json())
        assert update_res.status_code == 200
        assert update_res.json()["status"] == "Delivered"

    def test_invalid_tracking_number(self):
        response = client.get("/orders/tracking/INVALID123456")
        assert response.status_code == 404

        update_response = client.put("/orders/tracking/update", json={
            "tracking_number": "INVALID123456",
            "status": "Delivered"
        })
        assert update_response.status_code == 404
