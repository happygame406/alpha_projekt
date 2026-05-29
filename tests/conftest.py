import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from sqlmodel import SQLModel

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Создаём таблицы перед всеми тестами"""
    SQLModel.metadata.create_all(engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client