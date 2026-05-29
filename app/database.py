from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")

# Синхронный engine
engine = create_engine(DATABASE_URL, echo=True)

# Зависимость для FastAPI
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]