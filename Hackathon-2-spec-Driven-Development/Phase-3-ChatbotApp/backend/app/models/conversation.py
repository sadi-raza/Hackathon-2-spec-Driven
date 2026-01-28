"""
Conversation Model for Phase III Chatbot.

Represents a chat session between a user and the AI assistant.
Conversations contain multiple messages and belong to a single user.
"""

from sqlmodel import SQLModel, Field, Relationship, Index
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session.

    Attributes:
        id: Unique identifier (auto-increment integer)
        user_id: Foreign key to users table (user isolation)
        title: Optional conversation title (auto-generated from first message)
        created_at: Timestamp when conversation was created
        updated_at: Timestamp of last activity
    """
    __tablename__ = "conversations"

    __table_args__ = (
        Index("idx_conversations_user_id", "user_id"),
        Index("idx_conversations_user_updated", "user_id", "updated_at"),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str | None = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.utcnow()
