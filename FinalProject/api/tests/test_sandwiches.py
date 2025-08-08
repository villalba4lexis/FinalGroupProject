from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)

def generate_unique_name():
    return f"Test Sandwich {uuid.uuid4()}"

def test_create_sandwich():
    unique_name = generate_unique_name()
    response = client.post("/sandwiches/", json={
        "sandwich_name": unique_name,
        "calories": 500,
        "price": 7.99,
        "category": "Test Category"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["sandwich_name"] == unique_name
    assert float(data["price"]) == 7.99
    assert "id" in data
    return data["id"], unique_name

def test_read_sandwich():
    sandwich_id, name = test_create_sandwich()
    response = client.get(f"/sandwiches/{sandwich_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["sandwich_name"] == name

def test_read_all_sandwiches():
    response = client.get("/sandwiches/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_sandwich():
    sandwich_id, _ = test_create_sandwich()
    updated_name = generate_unique_name()
    response = client.put(f"/sandwiches/{sandwich_id}", json={
        "sandwich_name": updated_name,
        "calories": 600,
        "price": 8.99,
        "category": "Updated Category"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sandwich_name"] == updated_name
    assert float(data["price"]) == 8.99

def test_delete_sandwich():
    sandwich_id, _ = test_create_sandwich()
    response = client.delete(f"/sandwiches/{sandwich_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/sandwiches/{sandwich_id}")
    assert response.status_code == 404

