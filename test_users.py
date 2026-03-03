from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_create_user():
    response = client.post("/users", json={ "username": "TestUser1", "is_active": True })
    assert response.status_code == 200

def test_get_active_user():
    response = client.get("/users")
    assert response.status_code == 200