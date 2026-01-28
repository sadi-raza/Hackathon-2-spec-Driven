from sqlmodel import SQLModel, Field, Relationship, Index
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Define composite index for user_id and completed for filtered queries
    __table_args__ = (
        Index("idx_user_completed", "user_id", "completed"),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")