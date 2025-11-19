from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from src.modules.shared.models import TimestampModel

if TYPE_CHECKING:
    from src.modules.users.models import User


class Order(TimestampModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    total: float = Field(nullable=False)
    status: str = Field(default="pending")

    user: Optional["User"] = Relationship(back_populates="orders")
