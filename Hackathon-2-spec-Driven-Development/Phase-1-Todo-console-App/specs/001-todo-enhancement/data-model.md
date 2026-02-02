# Data Model: Todo Application Enhancement

**Feature**: 001-todo-enhancement
**Date**: 2025-12-30

## Entity: Task

**Description**: Represents a user task with enhanced attributes for organization and prioritization

**Fields**:
- `id: int` - Unique identifier for the task (auto-incremented)
- `title: str` - Title of the task (required, non-empty)
- `description: str` - Detailed description of the task (optional, can be empty)
- `status: str` - Current status of the task ("pending" or "completed", default "pending")
- `priority: str` - Priority level of the task ("high", "medium", "low", default "medium")
- `tags: list[str]` - List of tags associated with the task (default empty list)
- `created_at: datetime` - Timestamp when the task was created (automatically set)

**Validation Rules**:
- `title` must not be empty or None
- `priority` must be one of: "high", "medium", "low" (case-sensitive)
- `tags` must be a list of strings, with each tag being non-empty after stripping whitespace
- `status` must be one of: "pending", "completed" (case-sensitive)

**State Transitions**:
- `status` can transition from "pending" to "completed" when marked as done
- `status` can transition from "completed" to "pending" when unmarked
- Other fields can be updated during task modification

**Relationships**: None (standalone entity)

## Entity: FilterCriteria

**Description**: Represents criteria for filtering tasks

**Fields**:
- `status: Optional[str]` - Filter by status ("pending", "completed", "all", default None)
- `priority: Optional[str]` - Filter by priority ("high", "medium", "low", "all", default None)
- `tag: Optional[str]` - Filter by specific tag (default None)
- `combined: bool` - Whether to combine multiple filters (default True)

**Validation Rules**:
- `status` must be one of: "pending", "completed", "all", or None
- `priority` must be one of: "high", "medium", "low", "all", or None
- `tag` must be a non-empty string if provided

## Entity: SortCriteria

**Description**: Represents how tasks should be sorted

**Fields**:
- `field: str` - Field to sort by ("priority", "title", "created_at", default "created_at")
- `direction: str` - Sort direction ("asc", "desc", default "desc" for created_at, "asc" for others)

**Validation Rules**:
- `field` must be one of: "priority", "title", "created_at"
- `direction` must be one of: "asc", "desc"

## Entity: TaskSearchResult

**Description**: Represents the result of a task search operation

**Fields**:
- `tasks: List[Task]` - List of tasks matching the search criteria
- `query: str` - The search query that was used
- `total_count: int` - Total number of matching tasks
- `applied_filters: dict` - Dictionary of filters that were applied (if any)

## Priority Order Definition

**Priority Hierarchy** (for sorting purposes):
1. "high" (highest priority)
2. "medium" (medium priority)
3. "low" (lowest priority)