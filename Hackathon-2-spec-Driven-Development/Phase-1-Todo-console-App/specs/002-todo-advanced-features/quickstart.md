# Quickstart Guide: Todo App Advanced Features

## Overview
This guide provides a quick introduction to implementing the advanced features: recurring tasks, due dates, and time reminders.

## Implementation Steps

### 1. Extend Task Model
Update the Task dataclass in `src/models/task.py` to include new fields:
- `due_date: Optional[datetime] = None`
- `recurrence: Optional[str] = None`
- `recurrence_parent_id: Optional[int] = None`
- `is_recurring_template: bool = False`

### 2. Implement Date Utilities
Create `src/utils/date_utils.py` with:
- `parse_date_string(date_str: str) -> datetime` - Parse various date formats
- `calculate_next_date(current_date: datetime, recurrence_pattern: str) -> datetime` - Calculate next occurrence
- `format_datetime_for_display(dt: datetime) -> str` - Format for UI display

### 3. Enhance TodoManager
Update `src/services/todo_manager.py` with:
- Date parsing and formatting methods
- Recurrence handling methods (`generate_next_occurrence`, `get_recurring_tasks`)
- Reminder checking methods (`check_reminders`, `is_due_soon`, `is_overdue`)

### 4. Update CLI Interface
Enhance `src/cli/ui.py` with:
- New prompts for due dates and recurrence
- Enhanced task display with due date and recurrence columns
- New menu options for viewing overdue/due soon tasks

### 5. Integrate Reminder System
Add non-blocking reminder checks to the main application loop in `src/main.py`

## Key Features

### Recurring Tasks
- Create recurring tasks with daily, weekly, monthly, or yearly patterns
- Templates generate new instances automatically when completed
- Instances are linked to their templates via `recurrence_parent_id`

### Due Dates
- Support for absolute dates (YYYY-MM-DD) and relative dates ("tomorrow", "in 3 days")
- Flexible parsing handles multiple input formats
- Visual indicators for due soon (⏰) and overdue (❌) tasks

### Time Reminders
- Non-blocking periodic checks for upcoming tasks
- Console beep alerts for important reminders
- Visual highlighting of tasks needing attention

## Testing
- Unit tests for date parsing utilities
- Integration tests for recurrence logic
- UI tests for CLI enhancements