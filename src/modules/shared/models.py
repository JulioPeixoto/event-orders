from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
    )
