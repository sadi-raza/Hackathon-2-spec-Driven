from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..schemas.task import (
    TaskCreate, TaskUpdate, TaskToggle, TaskResponse,
    TaskListResponse, TaskDeleteResponse, TaskSchema
)
from ..services.task_service import TaskService
from ..database import get_db
from ..middleware.jwt import CurrentUser, get_current_user
from ..models.task import Task
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["tasks"])


def convert_task_to_schema(task: Task) -> TaskSchema:
    """Convert a Task model to TaskSchema for API responses."""
    return TaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        createdAt=task.created_at.isoformat(),
        updatedAt=task.updated_at.isoformat(),
        userId=task.user_id
    )


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """Create a new task for the authenticated user."""
    task_service = TaskService(db)

    task = await task_service.create_task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id
    )

    return TaskResponse(task=convert_task_to_schema(task))


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort: str = Query("created_at", description="Sort by field")
):
    """Get all tasks for the authenticated user."""
    task_service = TaskService(db)

    tasks = await task_service.get_tasks(
        user_id=current_user.id,
        completed=completed,
        sort=sort
    )

    task_schemas = [convert_task_to_schema(task) for task in tasks]
    total = len(task_schemas)

    return TaskListResponse(tasks=task_schemas, total=total)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_single_task(
    task_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific task by ID for the authenticated user."""
    task_service = TaskService(db)

    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(task=convert_task_to_schema(task))


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """Update a task for the authenticated user."""
    task_service = TaskService(db)

    updated_task = await task_service.update_task(
        task_id=task_id,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    if not updated_task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(task=convert_task_to_schema(updated_task))


@router.patch("/{task_id}", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: str,
    completion_data: TaskToggle,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """Toggle the completion status of a task for the authenticated user."""
    task_service = TaskService(db)

    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    # If we received specific completion status, update to that
    # Otherwise toggle the current status
    if completion_data.completed is not None:
        updated_task = await task_service.update_task(
            task_id=task_id,
            user_id=current_user.id,
            completed=completion_data.completed
        )
    else:
        # Toggle the completion status
        updated_task = await task_service.toggle_completion(task_id, current_user.id)

    if not updated_task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(task=convert_task_to_schema(updated_task))


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
async def delete_task(
    task_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """Delete a task for the authenticated user."""
    task_service = TaskService(db)

    deleted = await task_service.delete_task(task_id, current_user.id)
    if not deleted:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskDeleteResponse(message="Task deleted successfully")