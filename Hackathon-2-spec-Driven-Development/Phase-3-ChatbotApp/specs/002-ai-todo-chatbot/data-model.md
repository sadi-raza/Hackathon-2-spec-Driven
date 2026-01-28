# Data Model: AI-Powered Todo Chatbot

**Feature**: 002-ai-todo-chatbot
**Date**: 2025-01-16
**Status**: Complete

## Overview

Phase III extends the Phase II database with two new tables for conversation persistence while reusing the existing `Task` and `User` models.

---

## Existing Entities (Phase II - No Changes)

### User
```
Table: users
├── id: str (PK, UUID)
├── email: str (unique, indexed)
├── name: str
├── emailVerified: bool
├── image: str (optional)
├── createdAt: datetime
└── updatedAt: datetime
```

### Task
```
Table: tasks
├── id: str (PK, UUID)
├── user_id: str (FK → users.id, indexed)
├── title: str (max 200)
├── description: str (optional, max 1000)
├── completed: bool (indexed)
├── created_at: datetime
└── updated_at: datetime

Index: idx_user_completed (user_id, completed)
```

---

## New Entities (Phase III)

### Conversation

Represents a chat session between a user and the AI assistant.

```
Table: conversations
├── id: str (PK, UUID, auto-generated)
├── user_id: str (FK → users.id, indexed, NOT NULL)
├── title: str (optional, max 100) - Auto-generated from first message
├── created_at: datetime (default: now)
└── updated_at: datetime (default: now, auto-update)

Indexes:
├── idx_conversations_user_id (user_id)
└── idx_conversations_user_updated (user_id, updated_at DESC)

Relationships:
├── user: User (many-to-one)
└── messages: List[Message] (one-to-many, cascade delete)
```

**SQLModel Definition:**
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str | None = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    owner: "User" = Relationship(back_populates="conversations")
```

---

### Message

Represents a single message in a conversation (user or assistant).

```
Table: messages
├── id: str (PK, UUID, auto-generated)
├── conversation_id: str (FK → conversations.id, indexed, NOT NULL)
├── user_id: str (FK → users.id, indexed, NOT NULL)
├── role: str (enum: "user" | "assistant", NOT NULL)
├── content: str (NOT NULL, max 10000)
├── tool_calls: JSON (optional) - Array of tool call records
└── created_at: datetime (default: now)

Indexes:
├── idx_messages_conversation (conversation_id)
├── idx_messages_user (user_id)
└── idx_messages_conversation_created (conversation_id, created_at ASC)

Relationships:
├── conversation: Conversation (many-to-one)
└── user: User (many-to-one)
```

**SQLModel Definition:**
```python
from sqlalchemy import Column, JSON

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: MessageRole = Field(sa_column=Column(String, nullable=False))
    content: str = Field(max_length=10000)
    tool_calls: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

---

## Entity Relationships Diagram

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────┐
│    User     │       │  Conversation   │       │   Message   │
├─────────────┤       ├─────────────────┤       ├─────────────┤
│ id (PK)     │──┬───▶│ user_id (FK)    │       │ id (PK)     │
│ email       │  │    │ id (PK)         │──────▶│ conv_id(FK) │
│ name        │  │    │ title           │       │ user_id(FK) │
│ ...         │  │    │ created_at      │       │ role        │
└─────────────┘  │    │ updated_at      │       │ content     │
       │         │    └─────────────────┘       │ tool_calls  │
       │         │                              │ created_at  │
       │         └─────────────────────────────▶└─────────────┘
       │                                               ▲
       └───────────────────────────────────────────────┘

┌─────────────┐
│    Task     │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│◀── User.id
│ title       │
│ description │
│ completed   │
│ ...         │
└─────────────┘
```

---

## Validation Rules

### Conversation
- `user_id`: Required, must exist in users table
- `title`: Optional, max 100 chars, auto-generated from first message if null

### Message
- `conversation_id`: Required, must exist in conversations table
- `user_id`: Required, must match conversation's user_id (enforced in service)
- `role`: Required, must be "user" or "assistant"
- `content`: Required, 1-10000 chars
- `tool_calls`: Optional, valid JSON array when present

---

## Migration Notes

1. **No changes to existing tables** - Task and User remain unchanged
2. **New tables created on app startup** via SQLModel metadata.create_all
3. **Foreign key constraints** ensure referential integrity
4. **Cascade delete** - Deleting a Conversation deletes its Messages
5. **Indexes optimize** user-filtered queries (stateless design)

---

## Query Patterns

### Get user's conversations (most recent first)
```sql
SELECT * FROM conversations
WHERE user_id = :user_id
ORDER BY updated_at DESC
LIMIT 20;
```

### Get conversation messages (chronological)
```sql
SELECT * FROM messages
WHERE conversation_id = :conv_id
ORDER BY created_at ASC;
```

### Create new conversation with first message
```sql
-- Transaction
INSERT INTO conversations (id, user_id, title, created_at, updated_at)
VALUES (:id, :user_id, :title, NOW(), NOW());

INSERT INTO messages (id, conversation_id, user_id, role, content, created_at)
VALUES (:msg_id, :conv_id, :user_id, 'user', :content, NOW());
```
