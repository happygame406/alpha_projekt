from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# ==================== ТАБЛИЦА В БАЗЕ ====================
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    
    items: List["Item"] = Relationship(back_populates="owner", cascade_delete=True)

# ==================== Pydantic МОДЕЛИ ДЛЯ API ====================
class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=100)
    password: str

class UserOut(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UsersOut(SQLModel):
    users: List[UserOut]
    total: int

    class Config:
        from_attributes = True