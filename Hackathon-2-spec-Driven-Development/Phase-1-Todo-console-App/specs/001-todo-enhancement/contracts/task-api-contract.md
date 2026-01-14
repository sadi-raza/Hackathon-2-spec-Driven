# Task API Contract: Todo Application Enhancement

**Feature**: 001-todo-enhancement
**Date**: 2025-12-30

## Overview

This contract defines the API methods for the enhanced Todo application. Since this is a Phase I console application, these are internal method contracts rather than external API endpoints.

## Task Model Contract

### Task Class Definition
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "pending"  # "pending" or "completed"
    priority: str = "medium"  # "high", "medium", or "low"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
```

### Validation Rules
- `title` must not be empty
- `status` must be "pending" or "completed"
- `priority` must be "high", "medium", or "low"
- `tags` must be a list of non-empty strings

## TodoManager API Contract

### Method: add_task
**Input**: title: str, description: str, priority: str, tags: List[str]
**Output**: Task object with assigned ID
**Behavior**: Creates a new task with provided parameters, validates inputs, assigns ID and creation timestamp
**Success Criteria**: Returns valid Task object with unique ID
**Error Conditions**: Invalid priority or empty title raises ValueError

### Method: search_tasks
**Input**: query: str
**Output**: List[Task]
**Behavior**: Returns tasks containing query in title or description (case-insensitive)
**Success Criteria**: Returns matching tasks or empty list if none found
**Error Conditions**: None

### Method: filter_tasks
**Input**: status: Optional[str], priority: Optional[str], tag: Optional[str]
**Output**: List[Task]
**Behavior**: Returns tasks matching filter criteria
**Success Criteria**: Returns matching tasks or empty list if none found
**Error Conditions**: Invalid filter values raise ValueError

### Method: sort_tasks
**Input**: tasks: List[Task], field: str, direction: str
**Output**: List[Task]
**Behavior**: Returns tasks sorted by specified field
**Success Criteria**: Returns sorted task list
**Error Conditions**: Invalid field or direction raises ValueError

### Method: update_task
**Input**: task_id: int, **kwargs (title, description, status, priority, tags)
**Output**: Updated Task object
**Behavior**: Updates specified task fields
**Success Criteria**: Returns updated Task object
**Error Conditions**: Task not found raises ValueError

## CLI Interface Contract

### Menu Options
1. Add Task - prompts for title, description, priority, tags
2. View Tasks - displays all tasks with enhanced format
3. Update Task - allows modification of task fields
4. Mark Complete - changes task status to completed
5. Delete Task - removes task from list
6. Search Tasks - searches by keyword
7. Exit - exits application

### Enhanced Display Format
```
ID | Priority | Title | Tags | Status | Created
1  | 🔥 High  | Task Title | tag1, tag2 | ⏳ Pending | 2025-12-30
```

## Validation Contract

### Input Validation
- Priority: must be one of "high", "medium", "low"
- Tags: comma-separated string converted to list of non-empty strings
- Title: required, non-empty string
- Status: "pending" or "completed"

### Error Handling
- Invalid inputs should show clear error messages
- Invalid operations should not crash the application
- Empty results should display appropriate messages