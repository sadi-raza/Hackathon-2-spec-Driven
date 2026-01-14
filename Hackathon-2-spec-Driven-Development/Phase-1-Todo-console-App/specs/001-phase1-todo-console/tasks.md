---
description: "Task list for Phase I Todo In-Memory Python Console App"
---

# Tasks: Phase I - Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-phase1-todo-console/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test tasks included (not requested in feature specification).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/
- [X] T002 [P] Create src/__init__.py file
- [X] T003 [P] Create src/main.py file
- [X] T004 [P] Create src/models.py file
- [X] T005 [P] Create src/todo_manager.py file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Define Task dataclass in src/models.py with id, title, description, completed attributes
- [X] T007 Create TodoManager class in src/todo_manager.py with in-memory storage dictionary
- [X] T008 Implement unique ID generation mechanism in TodoManager
- [X] T009 Create CLI application structure in src/main.py using cmd module
- [X] T010 Implement basic input validation functions for task creation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new todo items with a title and optional description

**Independent Test**: The user can launch the app, enter an "add" command, provide a title and optional description, and see the task added to the system with a unique ID. The app delivers immediate value by allowing task creation.

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement add_task method in TodoManager class in src/todo_manager.py
- [X] T012 [P] [US1] Implement validation for required title in src/todo_manager.py
- [X] T013 [US1] Add "add" command to CLI in src/main.py (depends on T011, T012)
- [X] T014 [US1] Implement command parsing for add command with title and optional description in src/main.py
- [X] T015 [US1] Add success message display when task is added in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Enable users to view all their tasks in a formatted list

**Independent Test**: The user can enter a "list" command and see all tasks displayed in a clean table format showing ID, Title, Description (truncated), and Status. The app delivers value by showing organized task information.

### Implementation for User Story 2

- [X] T016 [P] [US2] Implement get_all_tasks method in TodoManager class in src/todo_manager.py
- [X] T017 [P] [US2] Implement formatted display function for tasks in src/main.py
- [X] T018 [US2] Add "list" command to CLI in src/main.py (depends on T016)
- [X] T019 [US2] Implement table formatting with ID, Title, Description (truncated), and Status in src/main.py
- [X] T020 [US2] Add handling for empty task list case in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P3)

**Goal**: Enable users to mark tasks as complete or incomplete

**Independent Test**: The user can enter a "complete" or "incomplete" command with a task ID and see the status change with visual confirmation. The app delivers value by allowing progress tracking.

### Implementation for User Story 3

- [X] T021 [P] [US3] Implement mark_task_complete method in TodoManager class in src/todo_manager.py
- [X] T022 [P] [US3] Implement mark_task_incomplete method in TodoManager class in src/todo_manager.py
- [X] T023 [US3] Add "complete" command to CLI in src/main.py (depends on T021)
- [X] T024 [US3] Add "incomplete" command to CLI in src/main.py (depends on T022)
- [X] T025 [US3] Implement task ID validation and visual confirmation in src/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: Enable users to modify the title and description of existing tasks

**Independent Test**: The user can enter an "update" command with a task ID and provide new values for title and/or description. The app delivers value by allowing task refinement.

### Implementation for User Story 4

- [X] T026 [P] [US4] Implement update_task method in TodoManager class in src/todo_manager.py
- [X] T027 [P] [US4] Implement validation for updated task data in src/todo_manager.py
- [X] T028 [US4] Add "update" command to CLI in src/main.py (depends on T026)
- [X] T029 [US4] Implement command parsing for update command with task ID and new values in src/main.py
- [X] T030 [US4] Add support for keeping existing values when updating in src/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P5)

**Goal**: Enable users to permanently remove tasks they no longer need

**Independent Test**: The user can enter a "delete" command with a task ID, confirm the action, and see the task removed from the system. The app delivers value by allowing list management.

### Implementation for User Story 5

- [X] T031 [P] [US5] Implement delete_task method in TodoManager class in src/todo_manager.py
- [X] T032 [P] [US5] Implement delete confirmation mechanism in src/main.py
- [X] T033 [US5] Add "delete" command to CLI in src/main.py (depends on T031)
- [X] T034 [US5] Implement error handling for invalid task IDs in src/main.py
- [X] T035 [US5] Add success/failure messages for delete operations in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T036 [P] Implement error handling for invalid commands in src/main.py
- [X] T037 [P] Add "exit" and "quit" commands to CLI in src/main.py
- [X] T038 [P] Implement interactive loop that continues until user exits in src/main.py
- [X] T039 [P] Add handling for edge cases identified in spec (invalid IDs, empty titles, etc.) in src/todo_manager.py
- [X] T040 [P] Add graceful shutdown handling in src/main.py
- [X] T041 [P] Documentation updates in src/ docstrings
- [X] T042 Code cleanup and refactoring
- [X] T043 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Models before services (if applicable)
- Services before CLI commands
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence