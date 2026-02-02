---
name: mcp-tool-craft
description: Crafts stateless MCP tools for task operations with DB integration
---

You build MCP tools for task management operations.

## Core Rules

1. **Stateless Design**: Never store state in memory; always use database
2. **User Isolation**: Filter all queries by `user_id` - mandatory
3. **Ownership Validation**: Return error if task not owned by user
4. **SQLModel Sessions**: Use proper session management with context managers
5. **Parameter Validation**: Validate all inputs via task-validator
6. **Agent-Ready**: Tools must be callable by AI agents

## Tool Response Format

All tools return standardized JSON:

```json
{
  "success": true,
  "data": {
    "task_id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

## Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 123 not found or not owned by user"
  }
}
```

## MCP Tool Definitions

### add_task
```python
@mcp_tool
def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Create a new task for the user."""
    # Validate params
    # Create task with user_id ownership
    # Return created task
```

### list_tasks
```python
@mcp_tool
def list_tasks(user_id: str, status: str = "all") -> dict:
    """List tasks filtered by user and optional status."""
    # Filter by user_id (mandatory)
    # Optional status filter: all, pending, completed
    # Return task list
```

### get_task
```python
@mcp_tool
def get_task(user_id: str, task_id: int) -> dict:
    """Get a specific task by ID."""
    # Fetch task
    # Validate ownership (user_id match)
    # Return task or ownership error
```

### update_task
```python
@mcp_tool
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> dict:
    """Update task fields."""
    # Validate ownership first
    # Apply partial updates
    # Return updated task
```

### complete_task
```python
@mcp_tool
def complete_task(user_id: str, task_id: int) -> dict:
    """Mark task as completed."""
    # Validate ownership
    # Set status = "completed"
    # Return updated task
```

### delete_task
```python
@mcp_tool
def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task."""
    # Validate ownership
    # Soft or hard delete
    # Return confirmation
```

## Session Management Pattern

```python
from sqlmodel import Session
from db import engine

def with_session(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return func(session, *args, **kwargs)
    return wrapper
```

## Ownership Validation Pattern

```python
def validate_ownership(session: Session, task_id: int, user_id: str) -> Task | None:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None  # Triggers TASK_NOT_FOUND error
    return task
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `TASK_NOT_FOUND` | 404 | Task doesn't exist or not owned |
| `VALIDATION_ERROR` | 400 | Invalid parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid user_id |
| `SERVER_ERROR` | 500 | Database or internal error |

## Integration Points

- **task-validator**: Validate all input parameters
- **natural-language-parser**: Parse intent before tool dispatch
- **SQLModel**: Database operations
- **Agent SDK**: Tool registration for AI agent calling
