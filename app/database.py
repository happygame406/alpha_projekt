from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")

# Синхронный engine (для простоты)
engine = create_engine(DATABASE_URL, echo=False)

# Зависимость для FastAPI
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]