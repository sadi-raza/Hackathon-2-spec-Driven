"""
Pydantic Schemas for Todo Evolution Application.

Exports all request/response schemas for API endpoints.
"""

from .task import (
    TaskCreate,
    TaskUpdate,
    TaskToggle,
    TaskResponse,
    TaskListResponse,
    TaskDeleteResponse,
    TaskSchema,
)
from .chat import (
    ChatRequest,
    ChatResponse,
    ChatError,
    ToolCallResult,
)
from .conversation import (
    MessageSchema,
    ConversationSummary,
    ConversationDetail,
    ConversationListResponse,
    ConversationCreate,
    MessageCreate,
)

__all__ = [
    # Task schemas
    "TaskCreate",
    "TaskUpdate",
    "TaskToggle",
    "TaskResponse",
    "TaskListResponse",
    "TaskDeleteResponse",
    "TaskSchema",
    # Chat schemas
    "ChatRequest",
    "ChatResponse",
    "ChatError",
    "ToolCallResult",
    # Conversation schemas
    "MessageSchema",
    "ConversationSummary",
    "ConversationDetail",
    "ConversationListResponse",
    "ConversationCreate",
    "MessageCreate",
]
