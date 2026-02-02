# Tasks: FastAPI Todo API Backend

**Input**: Design documents from `/specs/001-fastapi-todo-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Following plan.md structure: `/backend/app/` for source code

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, PyJWT dependencies in backend/requirements.txt
- [ ] T003 [P] Configure linting and formatting tools in backend/.flake8, backend/.pre-commit-config.yaml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework in backend/app/database.py
- [X] T005 [P] Implement JWT authentication framework in backend/app/middleware/jwt.py
- [X] T006 [P] Setup API routing and middleware structure in backend/app/main.py
- [X] T007 Create base models/entities that all stories depend on in backend/app/models/
- [X] T008 Configure error handling and logging infrastructure in backend/app/main.py
- [X] T009 Setup environment configuration management in backend/app/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a New Task (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks with title and optional description

**Independent Test**: Can be fully tested by authenticating a user and creating a task, then verifying it appears in the user's task list with correct data.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for POST /api/tasks in backend/tests/test_tasks.py
- [ ] T011 [P] [US1] Integration test for task creation journey in backend/tests/test_tasks.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Task model in backend/app/models/task.py
- [X] T013 [P] [US1] Create User model in backend/app/models/user.py
- [X] T014 [US1] Implement TaskService in backend/app/services/task_service.py (depends on T012, T013)
- [X] T015 [US1] Implement POST /api/tasks endpoint in backend/app/api/tasks.py
- [X] T016 [US1] Add validation and error handling for task creation
- [X] T017 [US1] Add request/response schemas in backend/app/schemas/task.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View My Tasks (Priority: P1)

**Goal**: Enable authenticated users to view all their tasks with optional filtering

**Independent Test**: Can be tested by creating multiple tasks for a user, then retrieving the list and verifying all tasks are returned with correct data.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for GET /api/tasks in backend/tests/test_tasks.py
- [ ] T019 [P] [US2] Integration test for task listing journey in backend/tests/test_tasks.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Add User model relationship to Task in backend/app/models/user.py
- [X] T021 [US2] Implement TaskService methods for listing tasks in backend/app/services/task_service.py
- [X] T022 [US2] Implement GET /api/tasks endpoint in backend/app/api/tasks.py
- [X] T023 [US2] Add filtering by completion status in backend/app/services/task_service.py
- [X] T024 [US2] Implement user isolation in task listing queries

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update a Task (Priority: P2)

**Goal**: Enable authenticated users to update their task details

**Independent Test**: Can be tested by creating a task, updating its title and description, then verifying the changes persist.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Contract test for PUT /api/tasks/{id} in backend/tests/test_tasks.py
- [ ] T026 [P] [US3] Integration test for task update journey in backend/tests/test_tasks.py

### Implementation for User Story 3

- [X] T027 [P] [US3] Add update methods to TaskService in backend/app/services/task_service.py
- [X] T028 [US3] Implement PUT /api/tasks/{id} endpoint in backend/app/api/tasks.py
- [X] T029 [US3] Add validation for task updates in backend/app/schemas/task.py
- [X] T030 [US3] Implement ownership verification for updates

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Complete/Uncomplete a Task (Priority: P2)

**Goal**: Enable authenticated users to toggle task completion status

**Independent Test**: Can be tested by creating a task, toggling its completion status, and verifying the status changes correctly each time.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Contract test for PATCH /api/tasks/{id} in backend/tests/test_tasks.py
- [ ] T032 [P] [US4] Integration test for task completion journey in backend/tests/test_tasks.py

### Implementation for User Story 4

- [X] T033 [P] [US4] Add toggle completion methods to TaskService in backend/app/services/task_service.py
- [X] T034 [US4] Implement PATCH /api/tasks/{id} endpoint in backend/app/api/tasks.py
- [X] T035 [US4] Add validation for completion updates in backend/app/schemas/task.py
- [X] T036 [US4] Implement ownership verification for completion toggles

**Checkpoint**: All user stories 1, 2, 3, and 4 should now be independently functional

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Enable authenticated users to delete their tasks permanently

**Independent Test**: Can be tested by creating a task, deleting it, then verifying it no longer appears in the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US5] Contract test for DELETE /api/tasks/{id} in backend/tests/test_tasks.py
- [ ] T038 [P] [US5] Integration test for task deletion journey in backend/tests/test_tasks.py

### Implementation for User Story 5

- [X] T039 [P] [US5] Add delete methods to TaskService in backend/app/services/task_service.py
- [X] T040 [US5] Implement DELETE /api/tasks/{id} endpoint in backend/app/api/tasks.py
- [X] T041 [US5] Implement ownership verification for deletions
- [X] T042 [US5] Add success response schema for deletion

**Checkpoint**: All user stories 1, 2, 3, 4, and 5 should now be independently functional

---

## Phase 8: User Story 6 - View Single Task Details (Priority: P3)

**Goal**: Enable authenticated users to view details of a specific task

**Independent Test**: Can be tested by creating a task with specific details, then retrieving it by ID and verifying all fields are returned correctly.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T043 [P] [US6] Contract test for GET /api/tasks/{id} in backend/tests/test_tasks.py
- [ ] T044 [P] [US6] Integration test for single task retrieval journey in backend/tests/test_tasks.py

### Implementation for User Story 6

- [X] T045 [P] [US6] Add get single task methods to TaskService in backend/app/services/task_service.py
- [X] T046 [US6] Implement GET /api/tasks/{id} endpoint in backend/app/api/tasks.py
- [X] T047 [US6] Implement ownership verification for single task retrieval
- [X] T048 [US6] Add response schema for single task in backend/app/schemas/task.py

**Checkpoint**: All user stories 1, 2, 3, 4, 5, and 6 should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T049 [P] Documentation updates in backend/README.md
- [X] T050 Code cleanup and refactoring across all modules
- [ ] T051 Performance optimization for database queries
- [ ] T052 [P] Additional unit tests in backend/tests/unit/
- [X] T053 Security hardening and validation
- [X] T054 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4/US5 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/tasks in backend/tests/test_tasks.py"
Task: "Integration test for task creation journey in backend/tests/test_tasks.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/app/models/task.py"
Task: "Create User model in backend/app/models/user.py"
```

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
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
   - Developer F: User Story 6
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence