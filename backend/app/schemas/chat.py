"""
Chat Schemas for Phase III Chatbot.

Request and response schemas for the chat endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any


class ToolCallResult(BaseModel):
    """Schema for a single tool call result."""
    tool: str = Field(..., description="Name of the tool called")
    success: bool = Field(..., description="Whether the tool call succeeded")
    result: Optional[str] = Field(default=None, description="Result message from the tool")


class ChatRequest(BaseModel):
    """
    Request schema for POST /api/{user_id}/chat endpoint.

    Attributes:
        message: The user's natural language message
        conversation_id: Optional conversation ID to continue existing conversation
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's natural language message"
    )
    conversation_id: Optional[int] = Field(
        default=None,
        description="Optional conversation ID to continue existing conversation"
    )


class ChatResponse(BaseModel):
    """
    Response schema for POST /api/{user_id}/chat endpoint.

    Attributes:
        conversation_id: The conversation ID (new or existing)
        response: The assistant's response message
        tool_calls: Array of tool calls made during processing
    """
    conversation_id: int = Field(..., description="The conversation ID")
    response: str = Field(..., description="The assistant's response message")
    tool_calls: list[ToolCallResult] = Field(
        default_factory=list,
        description="Array of tool calls made during processing"
    )


class ChatError(BaseModel):
    """Schema for chat error responses."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="User-friendly error message")
