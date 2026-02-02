# Data Model: Phase I - Todo In-Memory Python Console App

**Date**: 2025-12-30
**Feature**: Phase I - Todo In-Memory Python Console App
**Branch**: 001-phase1-todo-console

## Task Entity

### Attributes
- **id**: Integer (required, unique, auto-incremented)
  - Purpose: Unique identifier for each task
  - Constraints: Must be unique, positive integer
  - Validation: Positive integer, unique across all tasks

- **title**: String (required)
  - Purpose: The main task description
  - Constraints: Required, non-empty
  - Validation: Non-empty string, max length 255 characters

- **description**: String (optional)
  - Purpose: Additional details about the task
  - Constraints: Optional, can be empty
  - Validation: Max length 1000 characters, null/empty allowed

- **completed**: Boolean (required, default: False)
  - Purpose: Indicates completion status of the task
  - Constraints: Boolean value, defaults to False
  - Validation: Must be true or false

### Validation Rules
1. Title must be provided and not empty when creating a task
2. ID must be unique across all tasks
3. ID must be a positive integer
4. Description, if provided, should not exceed 1000 characters
5. Completed status must be a boolean value

### State Transitions
- **Initial State**: completed = False (when task is created)
- **Completed State**: completed = True (when task is marked as complete)
- **Incomplete State**: completed = False (when completed task is marked as incomplete)

### Relationships
- No relationships with other entities (standalone entity for Phase I)

### Business Rules
1. A task must have a title to be valid
2. Task ID is automatically assigned and cannot be modified
3. Task completion status can be toggled multiple times
4. Task details (title, description) can be updated after creation