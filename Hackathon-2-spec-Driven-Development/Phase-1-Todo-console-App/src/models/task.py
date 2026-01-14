from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a user task with enhanced attributes for organization and prioritization.
    """
    id: int
    title: str
    description: str = ""
    status: str = "pending"  # "pending" or "completed"
    priority: str = "medium"  # "high", "medium", or "low"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None  # Optional due date/time for the task
    recurrence: Optional[str] = None  # Recurrence pattern if task repeats ("daily", "weekly", "monthly", "yearly", "every_monday", etc.)
    recurrence_parent_id: Optional[int] = None  # ID of parent recurring template if this is an instance
    is_recurring_template: bool = False  # Flag indicating if this is a recurring template

    def __post_init__(self):
        """Validate the task after initialization."""
        self.validate()

    def validate(self):
        """Validate the task attributes."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title must not be empty")

        if self.status not in ["pending", "completed"]:
            raise ValueError(f"Status must be 'pending' or 'completed', got '{self.status}'")

        if self.priority not in ["high", "medium", "low"]:
            raise ValueError(f"Priority must be 'high', 'medium', or 'low', got '{self.priority}'")

        # Validate tags: each tag should be non-empty after stripping whitespace
        if self.tags:
            for tag in self.tags:
                if not tag or not tag.strip():
                    raise ValueError(f"Tags must be non-empty, got '{tag}'")

        # Validate recurrence field if provided
        if self.recurrence is not None:
            valid_recurrence_patterns = [
                "daily", "weekly", "monthly", "yearly",
                "every_monday", "every_tuesday", "every_wednesday",
                "every_thursday", "every_friday", "every_saturday", "every_sunday"
            ]
            if self.recurrence not in valid_recurrence_patterns:
                raise ValueError(f"Recurrence must be one of {valid_recurrence_patterns}, got '{self.recurrence}'")

        # Validate that is_recurring_template and recurrence_parent_id are mutually exclusive
        if self.is_recurring_template and self.recurrence_parent_id is not None:
            raise ValueError("A task cannot be both a recurring template and an instance of a recurring task")

    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "completed"

    def mark_pending(self):
        """Mark the task as pending."""
        self.status = "pending"

    def update_priority(self, new_priority: str):
        """Update the task priority after validation."""
        if new_priority not in ["high", "medium", "low"]:
            raise ValueError(f"Priority must be 'high', 'medium', or 'low', got '{new_priority}'")
        self.priority = new_priority

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate if the priority is one of the allowed values."""
        return priority in ["high", "medium", "low"]

    def add_tags(self, new_tags: List[str]):
        """Add new tags to the task after validation."""
        for tag in new_tags:
            if not tag or not tag.strip():
                raise ValueError(f"Tags must be non-empty, got '{tag}'")
        self.tags.extend(new_tags)
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in self.tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        self.tags = unique_tags

    @staticmethod
    def validate_tag(tag: str) -> bool:
        """Add tag validation to prevent empty or malformed tags."""
        return bool(tag and tag.strip())

    @staticmethod
    def process_tags_from_string(tags_string: str) -> List[str]:
        """Process comma-separated tags string into a list of validated tags."""
        if not tags_string:
            return []

        # Split by comma and clean each tag
        tags = [tag.strip() for tag in tags_string.split(",") if tag.strip()]

        # Validate each tag
        for tag in tags:
            if not Task.validate_tag(tag):
                raise ValueError(f"Invalid tag: '{tag}'")

        return tags

    def remove_tag(self, tag_to_remove: str):
        """Remove a specific tag from the task."""
        if tag_to_remove in self.tags:
            self.tags.remove(tag_to_remove)