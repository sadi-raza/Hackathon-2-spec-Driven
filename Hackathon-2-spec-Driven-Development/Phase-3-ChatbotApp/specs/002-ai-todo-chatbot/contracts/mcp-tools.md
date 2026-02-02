# MCP Tools Contract

**Feature**: 002-ai-todo-chatbot
**Date**: 2025-01-16

## Overview

Five stateless MCP tools exposed inside the FastAPI backend. All tools:
- Require `user_id` from JWT (user isolation enforced)
- Operate directly on Neon DB via SQLModel
- Return consistent response format
- Are stateless (no in-memory state)

---

## Tool 1: add_task

**Purpose**: Create a new task for the authenticated user.

### Signature
```python
@tool
async def add_task(
    user_id: str,       # From JWT, required
    title: str,         # Task title, required, max 200 chars
    description: str = None  # Optional, max 1000 chars
) -> dict
```

### Return Format
```json
{
  "task_id": "uuid-string",
  "status": "created",
  "title": "Task title"
}
```

### Error Cases
- Empty title → `{"error": "Title is required"}`
- Title too long → `{"error": "Title must be 200 characters or less"}`

---

## Tool 2: list_tasks

**Purpose**: List tasks for the authenticated user with optional status filter.

### Signature
```python
@tool
async def list_tasks(
    user_id: str,       # From JWT, required
    status: str = "all" # Filter: "all" | "pending" | "completed"
) -> dict
```

### Return Format
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Optional description",
      "completed": false,
      "created_at": "2025-01-16T10:00:00Z"
    }
  ],
  "total": 5,
  "filter": "all"
}
```

### Error Cases
- Invalid status → `{"error": "Status must be 'all', 'pending', or 'completed'"}`

---

## Tool 3: complete_task

**Purpose**: Mark a task as completed.

### Signature
```python
@tool
async def complete_task(
    user_id: str,       # From JWT, required
    task_id: str        # Task ID to complete, required
) -> dict
```

### Return Format
```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "title": "Task title"
}
```

### Error Cases
- Task not found → `{"error": "Task not found"}`
- Already completed → `{"task_id": "...", "status": "already_completed", "title": "..."}`

---

## Tool 4: delete_task

**Purpose**: Delete a task permanently.

### Signature
```python
@tool
async def delete_task(
    user_id: str,       # From JWT, required
    task_id: str        # Task ID to delete, required
) -> dict
```

### Return Format
```json
{
  "task_id": "uuid-string",
  "status": "deleted",
  "title": "Task title"
}
```

### Error Cases
- Task not found → `{"error": "Task not found"}`

---

## Tool 5: update_task

**Purpose**: Update a task's title and/or description.

### Signature
```python
@tool
async def update_task(
    user_id: str,           # From JWT, required
    task_id: str,           # Task ID to update, required
    title: str = None,      # New title, optional
    description: str = None # New description, optional
) -> dict
```

### Return Format
```json
{
  "task_id": "uuid-string",
  "status": "updated",
  "title": "Updated title"
}
```

### Error Cases
- Task not found → `{"error": "Task not found"}`
- No updates provided → `{"error": "No updates provided"}`
- Title too long → `{"error": "Title must be 200 characters or less"}`

---

## User Isolation Enforcement

All tools MUST:

1. Accept `user_id` as first parameter
2. Filter all DB queries by `user_id`
3. Never allow access to other users' tasks
4. Return "Task not found" for unauthorized access attempts

### Example Query Pattern
```python
async def get_task_for_user(db: AsyncSession, task_id: str, user_id: str):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Always include user_id filter
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()
```

---

## Tool Registration

Tools are registered with the MCP SDK and exposed to the OpenAI Agents SDK:

```python
from mcp import Tool, create_tools

tools = [
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
]

mcp_server = create_tools(tools)
```
