from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)

def generate_unique_resource_name():
    return f"Lettuce-{uuid.uuid4()}"

def test_create_resource():
    unique_name = generate_unique_resource_name()
    response = client.post("/resources/", json={
        "name": unique_name,
        "unit": "1"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == unique_name
    return data["id"], unique_name

def test_read_all_resources():
    response = client.get("/resources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_resource_by_id():
    resource_id, name = test_create_resource()
    response = client.get(f"/resources/{resource_id}")
    assert response.status_code == 200
    assert response.json()["name"] == name

def test_delete_resource():
    resource_id, _ = test_create_resource()
    response = client.delete(f"/resources/{resource_id}")
    assert response.status_code == 204

    # Confirm resource is gone
    response = client.get(f"/resources/{resource_id}")
    assert response.status_code == 404

def test_nonexistent_resource():
    # UUID unlikely to exist
    non_existing_id = 999999
    get_response = client.get(f"/resources/{non_existing_id}")
    assert get_response.status_code == 404

    delete_response = client.delete(f"/resources/{non_existing_id}")
    assert delete_response.status_code == 404
