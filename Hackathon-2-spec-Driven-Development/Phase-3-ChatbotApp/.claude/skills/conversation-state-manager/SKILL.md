---
name: conversation-state-manager
description: Manages conversation and message persistence in Neon DB
---

You handle conversation state with database-only persistence.

## Core Principle

**No server state** - All conversation data lives in Neon PostgreSQL. Server remains stateless.

## Data Models (SQLModel)

### Conversation
```python
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    title: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message
```python
class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    role: str  # "user" | "assistant" | "system"
    content: str
    tool_calls: dict | None = None  # JSON for tool invocations
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Methods

### create_conversation
```python
def create_conversation(user_id: str, title: str = None) -> Conversation:
    """Create new conversation, return conversation_id."""
    # Generate UUID
    # Set timestamps
    # Insert to DB
    # Return conversation object
```

### get_or_create_conversation
```python
def get_or_create_conversation(user_id: str, conversation_id: str = None) -> Conversation:
    """Get existing or create new conversation."""
    # If conversation_id provided:
    #   - Fetch and validate ownership
    #   - Return if owned, else error
    # If no conversation_id:
    #   - Create new conversation
    #   - Return new conversation
```

### get_conversation
```python
def get_conversation(conversation_id: str, user_id: str) -> Conversation | None:
    """Fetch conversation with ownership check."""
    # Query by conversation_id
    # Validate user_id matches
    # Return None if not owned (security)
```

### list_conversations
```python
def list_conversations(user_id: str, limit: int = 20, offset: int = 0) -> list[Conversation]:
    """List user's conversations, newest first."""
    # Filter by user_id
    # Order by updated_at DESC
    # Apply pagination
```

### store_message
```python
def store_message(
    conversation_id: str,
    role: str,
    content: str,
    tool_calls: dict = None
) -> Message:
    """Store a message in conversation."""
    # Validate role in ["user", "assistant", "system"]
    # Set created_at timestamp
    # Update conversation.updated_at
    # Insert message
    # Return message object
```

### get_message_history
```python
def get_message_history(
    conversation_id: str,
    user_id: str,
    limit: int = 50
) -> list[Message]:
    """Fetch message history array for conversation."""
    # Validate conversation ownership
    # Query messages by conversation_id
    # Order by created_at ASC
    # Apply limit
    # Return as array
```

### delete_conversation
```python
def delete_conversation(conversation_id: str, user_id: str) -> bool:
    """Delete conversation and all messages."""
    # Validate ownership
    # Cascade delete messages
    # Delete conversation
    # Return success
```

## Response Formats

### Message History Array
```json
{
  "conversation_id": "uuid-here",
  "messages": [
    {
      "id": "msg-uuid",
      "role": "user",
      "content": "Add task buy milk",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg-uuid",
      "role": "assistant",
      "content": "Task created successfully",
      "tool_calls": [{"name": "add_task", "params": {"title": "buy milk"}}],
      "created_at": "2024-01-15T10:30:01Z"
    }
  ]
}
```

### Conversation List
```json
{
  "conversations": [
    {
      "id": "uuid",
      "title": "Task management",
      "message_count": 12,
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 5,
  "limit": 20,
  "offset": 0
}
```

## Security Rules

1. **Always filter by user_id** - No exceptions
2. **Ownership validation** - Return None/error for non-owned resources
3. **No cross-user access** - Conversations are strictly isolated
4. **Timestamps immutable** - created_at never changes

## Session Pattern

```python
from sqlmodel import Session, select
from db import engine

def with_db_session(func):
    """Decorator for database operations."""
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
    return wrapper
```

## Integration Points

- **Neon PostgreSQL**: Primary data store
- **SQLModel**: ORM layer
- **mcp-tool-craft**: Tools use conversation context
- **natural-language-parser**: Messages parsed for intent
