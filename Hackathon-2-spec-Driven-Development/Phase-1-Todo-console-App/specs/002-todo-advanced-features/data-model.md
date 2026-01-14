# Data Model: Todo App Advanced Features

## Task Entity

### Fields
- `id: int` - Unique identifier for the task
- `title: str` - Task title/description
- `description: str` - Detailed task description (default: "")
- `status: str` - Task status ("pending" or "completed", default: "pending")
- `priority: str` - Task priority ("high", "medium", "low", default: "medium")
- `tags: List[str]` - List of tags for categorization (default: [])
- `created_at: datetime` - Timestamp when task was created (default: current time)
- `due_date: Optional[datetime]` - Optional due date/time for the task (default: None)
- `recurrence: Optional[str]` - Recurrence pattern if task repeats ("daily", "weekly", "monthly", "yearly", "every_monday", etc., default: None)
- `recurrence_parent_id: Optional[int]` - ID of parent recurring template if this is an instance (default: None)
- `is_recurring_template: bool` - Flag indicating if this is a recurring template (default: False)

### Relationships
- Recurring templates can generate multiple task instances
- Task instances reference their parent template via `recurrence_parent_id`

### Validation Rules
- All existing validation rules apply
- `due_date` must be a valid datetime if provided
- `recurrence` must be one of the supported patterns if provided
- `recurrence_parent_id` must reference an existing task if provided
- `is_recurring_template` and `recurrence_parent_id` are mutually exclusive (a task cannot be both a template and an instance)

### State Transitions
- Normal state transitions (pending ↔ completed) remain unchanged
- Recurring templates remain unchanged when instances are modified
- Completing a recurring task instance triggers generation of next occurrence