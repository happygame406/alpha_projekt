from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: int = Field(gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="items")

class ItemCreate(SQLModel):
    title: str = Field(min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: int = Field(gt=0)

class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

class ItemOut(SQLModel):
    id: int
    title: str
    description: Optional[str]
    price: int
    created_at: datetime
    user_id: int

class ItemsOut(SQLModel):
    items: List[ItemOut]
    total: int

    class Config:
        from_attributes = True