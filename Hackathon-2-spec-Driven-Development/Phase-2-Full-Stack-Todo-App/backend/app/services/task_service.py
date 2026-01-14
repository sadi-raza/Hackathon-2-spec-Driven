from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from typing import List, Optional
from datetime import datetime

from ..models.task import Task
from ..models.user import User


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(
        self,
        title: str,
        user_id: str,
        description: Optional[str] = None
    ) -> Task:
        """Create a new task for a user."""
        task = Task(
            title=title,
            description=description,
            user_id=user_id,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def get_tasks(
        self,
        user_id: str,
        completed: Optional[bool] = None,
        sort: str = "created_at"
    ) -> List[Task]:
        """Get all tasks for a user with optional filtering."""
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        if sort == "created_at":
            statement = statement.order_by(Task.created_at.desc())
        elif sort == "title":
            statement = statement.order_by(Task.title.asc())

        result = await self.db.execute(statement)
        tasks = result.scalars().all()

        return tasks

    async def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get a specific task by ID for a user (enforces ownership)."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )

        result = await self.db.execute(statement)
        task = result.scalar_one_or_none()

        return task

    async def update_task(
        self,
        task_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """Update a task for a user (enforces ownership)."""
        task = await self.get_task(task_id, user_id)
        if not task:
            return None

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def toggle_completion(self, task_id: str, user_id: str) -> Optional[Task]:
        """Toggle the completion status of a task (enforces ownership)."""
        task = await self.get_task(task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task for a user (enforces ownership)."""
        task = await self.get_task(task_id, user_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()

        return True

    async def get_task_count(self, user_id: str) -> int:
        """Get the count of tasks for a user."""
        statement = select(func.count(Task.id)).where(Task.user_id == user_id)
        result = await self.db.execute(statement)
        count = result.scalar()

        return count or 0