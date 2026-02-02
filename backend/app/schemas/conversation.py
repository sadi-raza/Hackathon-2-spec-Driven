"""
Conversation Schemas for Phase III Chatbot.

Schemas for conversation and message data transfer objects.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class MessageSchema(BaseModel):
    """Schema for a single message."""
    id: int = Field(..., description="Message ID")
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    tool_calls: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="Tool calls made in this message"
    )
    created_at: datetime = Field(..., description="Message creation timestamp")

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    """Schema for conversation list items."""
    id: int = Field(..., description="Conversation ID")
    title: Optional[str] = Field(default=None, description="Conversation title")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last activity timestamp")

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    """Schema for conversation with messages."""
    conversation: ConversationSummary = Field(..., description="Conversation info")
    messages: list[MessageSchema] = Field(
        default_factory=list,
        description="Messages in the conversation"
    )


class ConversationListResponse(BaseModel):
    """Response schema for listing conversations."""
    conversations: list[ConversationSummary] = Field(
        default_factory=list,
        description="List of conversations"
    )
    total: int = Field(..., description="Total number of conversations")


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation."""
    title: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional conversation title"
    )


class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Message content"
    )
    tool_calls: Optional[dict[str, Any]] = Field(
        default=None,
        description="Tool calls made in this message"
    )
