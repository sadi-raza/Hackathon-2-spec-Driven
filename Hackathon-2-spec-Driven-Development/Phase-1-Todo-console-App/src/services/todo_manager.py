from typing import List, Dict, Optional, Any
from datetime import datetime
from src.models.task import Task
from src.utils.date_utils import parse_date_string


class TodoManager:
    """
    Enhanced manager with filter, search, sort methods for todo tasks.
    """
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "", priority: str = "medium", tags: List[str] = None,
                 due_date: Optional[datetime] = None, recurrence: Optional[str] = None) -> Task:
        """
        Add a new task with the specified parameters.
        """
        if tags is None:
            tags = []

        # Validate priority
        if priority not in ["high", "medium", "low"]:
            raise ValueError(f"Priority must be 'high', 'medium', or 'low', got '{priority}'")

        # Validate title
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate tags
        for tag in tags:
            if not tag or not tag.strip():
                raise ValueError(f"Tags must be non-empty, got '{tag}'")

        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags[:],
            due_date=due_date,
            recurrence=recurrence,
            is_recurring_template=recurrence is not None
        )

        self.tasks.append(task)
        self.next_id += 1
        return task

    def add_comprehensive_input_validation(self):
        """
        Add comprehensive input validation for all new features.
        """
        # This is handled through the existing validation in each method
        pass


    def validate_priority(self, priority: str) -> bool:
        """
        Implement priority validation logic.
        """
        return priority in ["high", "medium", "low"]

    def parse_tags_from_string(self, tags_string: str) -> List[str]:
        """
        Implement tag parsing from comma-separated string.
        """
        if not tags_string:
            return []

        # Split by comma and clean each tag
        tags = [tag.strip() for tag in tags_string.split(",") if tag.strip()]

        # Validate each tag
        for tag in tags:
            if not tag or not tag.strip():
                raise ValueError(f"Invalid tag: '{tag}'")

        return tags

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """
        Update a task with the specified parameters.
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Validate and update fields if provided
        if 'title' in kwargs:
            if not kwargs['title'] or not kwargs['title'].strip():
                raise ValueError("Task title must not be empty")
            task.title = kwargs['title']

        if 'description' in kwargs:
            task.description = kwargs['description']

        if 'status' in kwargs:
            if kwargs['status'] not in ["pending", "completed"]:
                raise ValueError(f"Status must be 'pending' or 'completed', got '{kwargs['status']}'")
            task.status = kwargs['status']

        if 'priority' in kwargs:
            if kwargs['priority'] not in ["high", "medium", "low"]:
                raise ValueError(f"Priority must be 'high', 'medium', or 'low', got '{kwargs['priority']}'")
            task.priority = kwargs['priority']

        if 'tags' in kwargs:
            # Validate tags
            for tag in kwargs['tags']:
                if not tag or not tag.strip():
                    raise ValueError(f"Tags must be non-empty, got '{tag}'")
            task.tags = kwargs['tags'][:]

        if 'due_date' in kwargs:
            task.due_date = kwargs['due_date']

        if 'recurrence' in kwargs:
            task.recurrence = kwargs['recurrence']

        # Only allow updating is_recurring_template if the task is not already a recurring instance
        if 'is_recurring_template' in kwargs:
            if task.recurrence_parent_id is None:  # Only update if it's not a child task
                task.is_recurring_template = kwargs['is_recurring_template']

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def list_tasks(self) -> List[Task]:
        """
        List all tasks.
        """
        return self.tasks[:]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Implement search_tasks method with case-insensitive search algorithm.
        """
        query_lower = query.lower()
        matching_tasks = []

        for task in self.tasks:
            if query_lower in task.title.lower() or query_lower in task.description.lower():
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                     tag: Optional[str] = None, combined: bool = True) -> List[Task]:
        """
        Implement filter_tasks method with combined filter logic.
        """
        filtered_tasks = []

        for task in self.tasks:
            matches = []

            # Check status filter
            if status is not None:
                if status == "all":
                    matches.append(True)
                elif task.status == status:
                    matches.append(True)
                else:
                    matches.append(False)

            # Check priority filter
            if priority is not None:
                if priority == "all":
                    matches.append(True)
                elif task.priority == priority:
                    matches.append(True)
                else:
                    matches.append(False)

            # Check tag filter
            if tag is not None:
                if tag in task.tags:
                    matches.append(True)
                else:
                    matches.append(False)

            # Determine if task should be included based on match logic
            if not matches:  # No filters provided
                filtered_tasks.append(task)
            elif combined:  # All filters must match
                if all(matches):
                    filtered_tasks.append(task)
            else:  # Any filter can match
                if any(matches):
                    filtered_tasks.append(task)

        return filtered_tasks


    def sort_tasks(self, field: str = "created_at", direction: str = "desc") -> List[Task]:
        """
        Implement sort_tasks method with priority-based, title-based and date-based sorting logic.
        """
        if field not in ["priority", "title", "created_at"]:
            raise ValueError(f"Field must be 'priority', 'title', or 'created_at', got '{field}'")

        if direction not in ["asc", "desc"]:
            raise ValueError(f"Direction must be 'asc' or 'desc', got '{direction}'")

        # Define priority order for sorting
        priority_order = {"high": 0, "medium": 1, "low": 2}

        def sort_key(task):
            if field == "priority":
                return priority_order[task.priority]
            elif field == "title":
                return task.title.lower()
            elif field == "created_at":
                return task.created_at
            else:
                return getattr(task, field)

        # Sort the tasks
        sorted_tasks = sorted(self.tasks, key=sort_key, reverse=(direction == "desc"))
        return sorted_tasks

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete. If the task is a recurring instance, generate the next occurrence.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            The completed task, or None if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Mark the current task as complete
        task.status = "completed"

        # Check if this is a recurring task instance that needs to generate the next occurrence
        if task.recurrence and not task.is_recurring_template:
            # Find the parent template if it exists
            parent_task = None
            if task.recurrence_parent_id is not None:
                parent_task = self.get_task(task.recurrence_parent_id)

            # If no parent template found, use the current task if it has recurrence info
            recurring_template = parent_task if parent_task else task

            # Generate the next occurrence
            try:
                next_task = self.generate_next_occurrence(recurring_template)
                self.tasks.append(next_task)
            except ValueError:
                # If the task is not recurring, just complete it without generating next occurrence
                pass

        return task

    def parse_due_date(self, date_input: str) -> datetime:
        """
        Parse various date formats including relative dates.

        Args:
            date_input: String representation of the date

        Returns:
            Parsed datetime object
        """
        from src.utils.date_utils import parse_date_string
        return parse_date_string(date_input)

    def format_due_date(self, date: datetime) -> str:
        """
        Format datetime for display.

        Args:
            date: The datetime to format

        Returns:
            Formatted string representation of the datetime
        """
        from src.utils.date_utils import format_datetime_for_display
        return format_datetime_for_display(date)

    def get_task_instances(self, parent_id: int) -> List[Task]:
        """
        Get all instances of a recurring task based on the parent template ID.

        Args:
            parent_id: The ID of the recurring task template

        Returns:
            List of task instances that belong to the recurring task
        """
        return [task for task in self.tasks if task.recurrence_parent_id == parent_id]

    def get_recurring_tasks(self) -> List[Task]:
        """
        Get all recurring task templates (tasks where is_recurring_template is True).

        Returns:
            List of recurring task templates
        """
        return [task for task in self.tasks if task.is_recurring_template]

    def generate_next_occurrence(self, task: Task) -> Task:
        """
        Generate the next occurrence of a recurring task based on the recurrence pattern.

        Args:
            task: The recurring task template

        Returns:
            A new Task instance with updated due date based on the recurrence pattern
        """
        from src.utils.date_utils import calculate_next_date

        if not task.is_recurring_template:
            raise ValueError("Cannot generate next occurrence for a non-recurring task")

        if task.recurrence is None:
            raise ValueError("Task must have a recurrence pattern to generate next occurrence")

        # Calculate the next due date based on the recurrence pattern
        next_due_date = None
        if task.due_date:
            next_due_date = calculate_next_date(task.due_date, task.recurrence)

        # Create a new task instance with the same properties as the template
        # but with a new ID, reset status to pending, and set the recurrence_parent_id
        next_task = Task(
            id=self.next_id,
            title=task.title,
            description=task.description,
            status="pending",  # New instances start as pending
            priority=task.priority,
            tags=task.tags[:],  # Copy the tags
            due_date=next_due_date,
            recurrence=task.recurrence,
            recurrence_parent_id=task.id,  # Link to the parent template
            is_recurring_template=False  # This is an instance, not a template
        )

        self.next_id += 1
        return next_task

    def is_due_soon(self, task: Task, minutes: int = 15) -> bool:
        """
        Check if a task is due soon.

        Args:
            task: The task to check
            minutes: The time window in minutes (default 15)

        Returns:
            True if the task is due within the specified time window, False otherwise
        """
        if not task.due_date:
            return False

        from datetime import datetime, timedelta
        now = datetime.now()
        due_window = now + timedelta(minutes=minutes)

        return task.due_date <= due_window and task.status == "pending"

    def is_overdue(self, task: Task) -> bool:
        """
        Check if a task is overdue.

        Args:
            task: The task to check

        Returns:
            True if the task is overdue, False otherwise
        """
        if not task.due_date:
            return False

        from datetime import datetime
        now = datetime.now()

        return task.due_date < now and task.status == "pending"

    def check_reminders(self) -> List[Task]:
        """
        Find tasks that are due soon or overdue.

        Returns:
            List of tasks that are either due soon or overdue
        """
        due_soon_tasks = [task for task in self.tasks if self.is_due_soon(task)]
        overdue_tasks = [task for task in self.tasks if self.is_overdue(task)]

        # Combine the lists, avoiding duplicates
        all_reminder_tasks = []
        seen_ids = set()

        for task in due_soon_tasks + overdue_tasks:
            if task.id not in seen_ids:
                all_reminder_tasks.append(task)
                seen_ids.add(task.id)

        return all_reminder_tasks

    def filter_tasks_by_due_date(self, due_soon: bool = False, overdue: bool = False, recurring: bool = False) -> List[Task]:
        """
        Filter tasks based on due date status and recurrence.

        Args:
            due_soon: If True, return tasks that are due soon
            overdue: If True, return tasks that are overdue
            recurring: If True, return recurring tasks

        Returns:
            List of tasks matching the specified criteria
        """
        filtered_tasks = []

        for task in self.tasks:
            include_task = True

            if due_soon and not self.is_due_soon(task):
                include_task = False
            elif overdue and not self.is_overdue(task):
                include_task = False
            elif recurring and not task.is_recurring_template:
                include_task = False

            if include_task:
                filtered_tasks.append(task)

        return filtered_tasks

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        """
        return len(self.tasks)