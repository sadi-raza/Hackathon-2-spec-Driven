"""
Message Model for Phase III Chatbot.

Represents a single message in a conversation (user or assistant).
Messages belong to a conversation and store the content and metadata.
"""

from sqlmodel import SQLModel, Field, Relationship, Index, Column
from sqlalchemy import JSON, String
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any
from enum import Enum

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, Enum):
    """Enum for message roles in a conversation."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Message entity representing a single chat message.

    Attributes:
        id: Unique identifier (auto-increment integer)
        conversation_id: Foreign key to conversations table
        user_id: Foreign key to users table (for user isolation)
        role: Message role (user or assistant)
        content: Message content text
        tool_calls: Optional JSON array of tool calls made
        created_at: Timestamp when message was created
    """
    __tablename__ = "messages"

    __table_args__ = (
        Index("idx_messages_conversation", "conversation_id"),
        Index("idx_messages_user", "user_id"),
        Index("idx_messages_conversation_created", "conversation_id", "created_at"),
    )

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    role: str = Field(sa_column=Column(String(20), nullable=False))
    content: str = Field(max_length=10000)
    tool_calls: Optional[dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
