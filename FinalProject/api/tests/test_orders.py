from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)


def generate_unique_name(base: str = "John Doe") -> str:
    return f"{base} {uuid.uuid4()}"


def test_create_order():
    unique_name = generate_unique_name()
    response = client.post("/orders/", json={
        "customer_name": unique_name,
        "description": "Test order"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == unique_name
    assert data["description"] == "Test order"
    return data["id"], unique_name


def test_read_order_by_id():
    order_id, name = test_create_order()
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == name


def test_read_all_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_order():
    order_id, _ = test_create_order()
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404


def test_nonexistent_order():
    fake_id = 999999
    response = client.get(f"/orders/{fake_id}")
    assert response.status_code == 404

