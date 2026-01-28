"""
MCP Tools for Phase III Todo Chatbot.

Provides stateless tool definitions for task operations.
Each tool operation requires user_id for ownership enforcement.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.task_service import TaskService


async def add_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> dict:
    """
    Add a new task for the user.

    Args:
        db: Database session
        user_id: User ID for ownership
        title: Task title (required)
        description: Task description (optional)

    Returns:
        Dictionary with task details and success status
    """
    task_service = TaskService(db)

    task = await task_service.create_task(
        title=title,
        description=description,
        user_id=user_id
    )

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "message": f"Task '{title}' added successfully"
    }


async def list_tasks(
    db: AsyncSession,
    user_id: int,
    completed: Optional[bool] = None
) -> dict:
    """
    List all tasks for the user.

    Args:
        db: Database session
        user_id: User ID for ownership
        completed: Optional filter for completion status

    Returns:
        Dictionary with list of tasks
    """
    task_service = TaskService(db)

    tasks = await task_service.get_tasks(
        user_id=user_id,
        completed=completed
    )

    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat()
        }
        for task in tasks
    ]

    return {
        "success": True,
        "tasks": task_list,
        "total": len(task_list),
        "message": f"Found {len(task_list)} task(s)"
    }


async def complete_task(
    db: AsyncSession,
    user_id: int,
    task_id: int
) -> dict:
    """
    Mark a task as completed.

    Args:
        db: Database session
        user_id: User ID for ownership
        task_id: Task ID to complete

    Returns:
        Dictionary with result status
    """
    task_service = TaskService(db)

    task = await task_service.update_task(
        task_id=task_id,
        user_id=user_id,
        completed=True
    )

    if not task:
        return {
            "success": False,
            "error": "Task not found",
            "message": "Could not find the task to complete"
        }

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "message": f"Task '{task.title}' marked as completed"
    }


async def delete_task(
    db: AsyncSession,
    user_id: int,
    task_id: int
) -> dict:
    """
    Delete a task.

    Args:
        db: Database session
        user_id: User ID for ownership
        task_id: Task ID to delete

    Returns:
        Dictionary with result status
    """
    task_service = TaskService(db)

    # Get task title before deletion for confirmation message
    task = await task_service.get_task(task_id, user_id)
    if not task:
        return {
            "success": False,
            "error": "Task not found",
            "message": "Could not find the task to delete"
        }

    title = task.title
    deleted = await task_service.delete_task(task_id, user_id)

    if not deleted:
        return {
            "success": False,
            "error": "Delete failed",
            "message": "Could not delete the task"
        }

    return {
        "success": True,
        "task_id": task_id,
        "title": title,
        "message": f"Task '{title}' deleted successfully"
    }


async def update_task(
    db: AsyncSession,
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update a task's title and/or description.

    Args:
        db: Database session
        user_id: User ID for ownership
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dictionary with result status
    """
    task_service = TaskService(db)

    if not title and not description:
        return {
            "success": False,
            "error": "No updates provided",
            "message": "Please specify a new title or description"
        }

    task = await task_service.update_task(
        task_id=task_id,
        user_id=user_id,
        title=title,
        description=description
    )

    if not task:
        return {
            "success": False,
            "error": "Task not found",
            "message": "Could not find the task to update"
        }

    return {
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "message": f"Task '{task.title}' updated successfully"
    }


def get_mcp_tools() -> list:
    """Return the list of MCP tool definitions for agent registration."""
    return TOOL_DEFINITIONS


# Tool definitions for the agent
TOOL_DEFINITIONS = [
    {
        "name": "add_task",
        "description": "Add a new task to the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task to add"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description for the task"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "List all tasks in the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status (true for completed, false for pending)"
                }
            },
            "required": []
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to mark as completed"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task from the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task"
                }
            },
            "required": ["task_id"]
        }
    }
]
