from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)

def generate_unique_name(base: str = "Test Sandwich") -> str:
    return f"{base} {uuid.uuid4()}"

def test_create_recipe():
    # Prerequisites: create a sandwich and a resource
    sandwich_res = client.post("/sandwiches/", json={
        "sandwich_name": generate_unique_name(),
        "calories": 400,
        "price": 6.99,
        "category": "Test"
    })
    print("SANDWICH RESPONSE:", sandwich_res.status_code, sandwich_res.json())
    assert sandwich_res.status_code == 201
    sandwich = sandwich_res.json()

    resource_res = client.post("/resources/", json={
        "name": generate_unique_name("Tomato"),
        "unit": 1
    })
    print("RESOURCE RESPONSE:", resource_res.status_code, resource_res.json())
    assert resource_res.status_code == 201
    resource = resource_res.json()

    # Create recipe
    response = client.post("/recipes/", json={
        "sandwich_id": sandwich["id"],
        "resource_id": resource["id"],
        "amount": 2
    })
    print("RECIPE RESPONSE:", response.status_code, response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["sandwich"]["id"] == sandwich["id"]
    assert data["resource"]["id"] == resource["id"]
    return data["id"]

def test_read_all_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_recipe_by_id():
    recipe_id = test_create_recipe()
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert "sandwich" in response.json()

def test_delete_recipe():
    recipe_id = test_create_recipe()
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204
