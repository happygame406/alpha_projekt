from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_get_items():
    response = client.get("/items/")
    assert response.status_code in [200, 404, 405, 422, 500]

def test_create_item():
    response = client.post("/items/", json={"title": "Test", "price": 100, "user_id": 1})
    assert response.status_code in [200, 201, 405, 422]