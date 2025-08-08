from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)

def test_create_review_and_fetch():
    # Unique sandwich name to avoid conflicts
    sandwich_name = f"Review Me {uuid.uuid4()}"

    # Create a sandwich
    sandwich_res = client.post("/sandwiches/", json={
        "sandwich_name": sandwich_name,
        "calories": 550,
        "price": 8.75,
        "category": "Test"
    })
    assert sandwich_res.status_code == 201
    sandwich_id = sandwich_res.json()["id"]

    # Submit a review
    review_res = client.post("/reviews/", json={
        "sandwich_id": sandwich_id,
        "user_id": 1,
        "rating": 4.5,
        "comment": "Delicious!"
    })
    assert review_res.status_code == 201
    review_data = review_res.json()
    assert review_data["rating"] == 4.5
    assert review_data["comment"] == "Delicious!"
    assert review_data["sandwich_id"] == sandwich_id

    # Fetch reviews for the sandwich
    get_res = client.get(f"/reviews/sandwich/{sandwich_id}")
    assert get_res.status_code == 200
    reviews = get_res.json()
    assert isinstance(reviews, list)
    assert any(r["comment"] == "Delicious!" and r["sandwich_id"] == sandwich_id for r in reviews)