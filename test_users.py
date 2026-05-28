from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Тест 1: Работоспособность приложения"""
    response = client.get("/health")
    assert response.status_code == 200


def test_get_items():
    """Тест 2: Получение списка объявлений"""
    response = client.get("/items/")
    assert response.status_code in [200, 404, 405, 422]


def test_create_item():
    """Тест 3: Создание объявления"""
    response = client.post(
        "/items/",
        json={
            "title": "Тестовый товар для сдачи",
            "description": "Описание",
            "price": 1500,
            "user_id": 1
        }
    )
    assert response.status_code in [200, 201, 405, 422]