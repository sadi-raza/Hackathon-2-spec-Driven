"""
Data models for the Todo Console Application.

This module defines the Task dataclass used throughout the application.
"""
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier for the task
        title: Required string (the main task description)
        description: Optional string (additional details about the task)
        completed: Boolean flag indicating completion status (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False