"""
Todo Manager for the Todo Console Application.

This module implements the core business logic for managing tasks in memory.
"""
from typing import Dict, List, Optional
from models import Task


class TodoManager:
    """
    Manages tasks in memory with CRUD operations.
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and optional description.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The created Task object
        """
        if not title:
            raise ValueError("Task title cannot be empty")

        task_id = self._next_id
        self._next_id += 1

        task = Task(id=task_id, title=title, description=description, completed=False)
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            A list of all Task objects
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object if successful, None if task not found
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        if title is not None:
            if title == "":
                raise ValueError("Task title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            True if successful, False if task not found
        """
        if task_id not in self._tasks:
            return False

        self._tasks[task_id].completed = True
        return True

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            True if successful, False if task not found
        """
        if task_id not in self._tasks:
            return False

        self._tasks[task_id].completed = False
        return True