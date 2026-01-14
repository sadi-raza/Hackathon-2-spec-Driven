# Implementation Tasks: Todo App Advanced Features - Recurring Tasks, Due Dates & Time Reminders

**Feature**: Todo App Advanced Features | **Branch**: 002-todo-advanced-features | **Date**: 2025-12-30

## Phase 1: Setup Tasks

- [x] T001 Create utils directory for shared utilities
- [x] T002 Install dateutil library for date parsing in requirements.txt
- [x] T003 Create src/utils/__init__.py file

## Phase 2: Foundational Tasks

- [x] T004 [P] Update Task model with new fields in src/models/task.py
- [x] T005 [P] Create date utilities module in src/utils/date_utils.py
- [x] T006 [P] Update TodoManager imports to include new datetime functionality

## Phase 3: User Story 1 - Create Recurring Tasks (Priority: P1)

**Goal**: Implement recurring tasks functionality with template/instance pattern and auto-generation of next occurrences.

**Independent Test**: Can be fully tested by creating a recurring task with a specific pattern and verifying that it continues to appear in the task list according to the recurrence schedule, delivering consistent value for recurring activities.

**Tasks**:

### Models & Data Layer
- [x] T007 [P] [US1] Update Task model validation to handle new recurrence fields in src/models/task.py

### Service Layer
- [x] T008 [P] [US1] Implement generate_next_occurrence method in src/services/todo_manager.py
- [x] T009 [P] [US1] Implement get_recurring_tasks method in src/services/todo_manager.py
- [x] T010 [P] [US1] Implement get_task_instances method in src/services/todo_manager.py
- [x] T011 [US1] Update mark_task_complete logic to handle recurring tasks in src/services/todo_manager.py

### Date Utilities
- [x] T012 [P] [US1] Implement calculate_next_date function in src/utils/date_utils.py

### CLI Interface
- [x] T013 [P] [US1] Create prompt_for_recurrence method in src/cli/ui.py
- [x] T014 [US1] Update add_task method to include recurrence prompts in src/cli/ui.py
- [x] T015 [US1] Update display_task method to show recurrence indicators in src/cli/ui.py

## Phase 4: User Story 2 - Set Due Dates & Times (Priority: P1)

**Goal**: Implement flexible due date/time support with multiple input formats.

**Independent Test**: Can be fully tested by adding tasks with various due date formats (absolute and relative) and verifying they appear in the correct chronological order, delivering time-based organization value.

**Tasks**:

### Service Layer
- [x] T016 [P] [US2] Implement parse_due_date method in src/services/todo_manager.py
- [x] T017 [P] [US2] Implement format_due_date method in src/services/todo_manager.py
- [x] T018 [US2] Update add_task method to accept due_date parameter in src/services/todo_manager.py
- [x] T019 [US2] Update update_task method to handle due_date updates in src/services/todo_manager.py

### Date Utilities
- [x] T020 [P] [US2] Implement parse_date_string function in src/utils/date_utils.py
- [x] T021 [P] [US2] Implement format_datetime_for_display function in src/utils/date_utils.py

### CLI Interface
- [x] T022 [P] [US2] Create prompt_for_due_date method in src/cli/ui.py
- [x] T023 [US2] Update add_task method to include due date prompts in src/cli/ui.py
- [x] T024 [US2] Update update_task method to handle due date updates in src/cli/ui.py
- [x] T025 [US2] Update display_task method to show due dates in src/cli/ui.py

## Phase 5: User Story 3 - Receive Time Reminders (Priority: P2)

**Goal**: Implement console-based time reminders for tasks that are due soon or overdue.

**Independent Test**: Can be fully tested by setting up tasks with due dates and verifying that reminder notifications appear when the app is running and tasks approach their due time, delivering proactive notification value.

**Tasks**:

### Service Layer
- [x] T026 [P] [US3] Implement check_reminders method in src/services/todo_manager.py
- [x] T027 [P] [US3] Implement is_due_soon method in src/services/todo_manager.py
- [x] T028 [P] [US3] Implement is_overdue method in src/services/todo_manager.py

### CLI Interface
- [x] T029 [P] [US3] Update display_tasks method to highlight due/overdue tasks in src/cli/ui.py
- [x] T030 [US3] Create display_reminder_notifications method in src/cli/ui.py
- [x] T031 [US3] Add View Overdue/Due Soon menu option in src/cli/ui.py
- [x] T032 [US3] Update main menu to show reminder count in src/cli/ui.py

### Main Application Loop
- [x] T033 [US3] Integrate non-blocking reminder checks into main loop in src/main.py

## Phase 6: Integration & Enhancement Tasks

- [x] T034 [P] Update task display table format to include due date and recurrence columns in src/cli/ui.py
- [x] T035 [P] Add visual indicators (⏰, ❌, 🔄) for due soon, overdue, and recurring tasks in src/cli/ui.py
- [x] T036 Implement console beep alerts for reminders in src/cli/ui.py
- [x] T037 Update View Tasks submenu to include due date filtering options in src/cli/ui.py
- [x] T038 Test that all previous basic and intermediate features continue to work in src/services/todo_manager.py

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T039 Add comprehensive error handling for date parsing in src/utils/date_utils.py
- [x] T040 Add input validation for recurrence patterns in src/services/todo_manager.py
- [x] T041 Update documentation and docstrings for new methods in all files
- [x] T042 Test edge cases for recurring tasks (modification, deletion) in src/services/todo_manager.py
- [x] T043 Add unit tests for new functionality in tests/ directory
- [x] T044 Perform integration testing of all features together

## Dependencies

- **User Story 1 (Recurring Tasks)**: Depends on foundational Task model updates (T004) and date utilities (T005)
- **User Story 2 (Due Dates)**: Depends on foundational Task model updates (T004) and date utilities (T005)
- **User Story 3 (Reminders)**: Depends on User Story 2 (due dates) and date utilities (T005)

## Parallel Execution Examples

- **US1 Parallel Tasks**: T008 (generate_next_occurrence), T009 (get_recurring_tasks), T010 (get_task_instances), T013 (prompt_for_recurrence) can run in parallel
- **US2 Parallel Tasks**: T016 (parse_due_date), T017 (format_due_date), T020 (parse_date_string), T021 (format_datetime_for_display) can run in parallel
- **US3 Parallel Tasks**: T026 (check_reminders), T027 (is_due_soon), T028 (is_overdue), T029 (update display) can run in parallel

## Implementation Strategy

1. **MVP Scope**: Implement User Story 1 (Recurring Tasks) completely as minimum viable product
2. **Incremental Delivery**: Add User Story 2 (Due Dates) as second increment
3. **Final Enhancement**: Add User Story 3 (Reminders) as final increment
4. **Cross-cutting**: Address polish and integration concerns last