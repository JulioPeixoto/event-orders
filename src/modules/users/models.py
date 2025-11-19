from typing import Optional, List
from sqlmodel import Field, Relationship
from src.modules.shared.models import TimestampModel
from src.modules.orders.models import Order


class User(TimestampModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)

    orders: List["Order"] = Relationship(back_populates="user")
