from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()

# Основная БД
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
engine = create_engine(DATABASE_URL, echo=False)

# Тестовая БД (SQLite в памяти)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
test_engine = create_engine(TEST_DATABASE_URL, echo=False)

# Для обычных запросов
def get_session():
    with Session(engine) as session:
        yield session

# Для тестов
def get_test_session():
    with Session(test_engine) as session:
        yield session