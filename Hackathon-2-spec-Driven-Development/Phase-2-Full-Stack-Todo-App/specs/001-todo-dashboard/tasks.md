# Tasks: Phase II Todo Dashboard Frontend

**Input**: Design documents from `/specs/001-todo-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/api-contract.md

**Tests**: Tests are NOT explicitly requested in the spec. Tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` at repository root
- Paths shown below use the frontend structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure - must complete before any user story work

- [X] T001 Initialize Next.js 15.1+ project with TypeScript in frontend/ directory
- [X] T002 Install dependencies: react-query, zod, react-hook-form, sonner, next-themes, lucide-react in frontend/package.json
- [X] T003 [P] Configure TypeScript strict mode in frontend/tsconfig.json
- [X] T004 [P] Configure Tailwind CSS v4 in frontend/tailwind.config.ts
- [X] T005 Create globals.css with CSS variables for light/dark themes in frontend/styles/globals.css
- [X] T006 [P] Create TypeScript types for User, Task, AuthState, API responses in frontend/types/index.ts
- [X] T007 [P] Create Zod validation schemas for login, signup, task forms in frontend/validations/schemas.ts
- [X] T008 [P] Create utility functions (cn for classnames) in frontend/lib/utils.ts

**Checkpoint**: Project structure ready, dependencies installed, base configuration complete

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T009 Create API client class with JWT handling and 401 redirect in frontend/lib/api.ts
- [X] T010 Create auth utilities (setToken, getToken, clearAuth) in frontend/lib/auth.ts
- [X] T011 [P] Create QueryProvider component wrapping React Query in frontend/components/providers/QueryProvider.tsx
- [X] T012 [P] Create ThemeProvider component wrapping next-themes in frontend/components/providers/ThemeProvider.tsx
- [X] T013 [P] Create ToastProvider component with Sonner in frontend/components/providers/ToastProvider.tsx
- [X] T014 Create root layout with all providers and metadata in frontend/app/layout.tsx
- [X] T015 Create landing page with redirect logic to /dashboard or /login in frontend/app/page.tsx
- [X] T016 [P] Create global error boundary with recovery UI in frontend/app/global-error.tsx
- [X] T017 [P] Create custom 404 page in frontend/app/not-found.tsx
- [X] T018 [P] Create Button UI component with variants in frontend/components/ui/button.tsx
- [X] T019 [P] Create Input UI component with validation states in frontend/components/ui/input.tsx
- [X] T020 [P] Create Skeleton UI component for loading states in frontend/components/ui/skeleton.tsx
- [X] T021 [P] Create Card UI component in frontend/components/ui/card.tsx
- [X] T022 [P] Create Checkbox UI component in frontend/components/ui/checkbox.tsx
- [X] T023 [P] Create Modal UI component in frontend/components/ui/modal.tsx

**Checkpoint**: Foundation ready - all base components, providers, and API client available. User story implementation can now begin.

---

## Phase 3: User Story 1 - User Authentication (Priority: P1)

**Goal**: Allow users to sign up, log in, and log out securely with JWT authentication

**Independent Test**: Create account with email/password, logout, login again. Verify redirect to dashboard on success.

### Implementation for User Story 1

- [X] T024 [US1] Create auth layout with centered glass effect container in frontend/app/(auth)/layout.tsx
- [X] T025 [US1] Create useAuth hook with authentication state management in frontend/hooks/useAuth.ts
- [X] T026 [P] [US1] Create login page with form, validation, and API integration in frontend/app/(auth)/login/page.tsx
- [X] T027 [P] [US1] Create signup page with form, validation, and API integration in frontend/app/(auth)/signup/page.tsx
- [X] T028 [US1] Create ThemeToggle component for dark/light mode switch in frontend/components/ThemeToggle.tsx
- [X] T029 [US1] Create Header component with user email, theme toggle, logout in frontend/components/Header.tsx
- [X] T030 [US1] Create protected layout with auth guard and Header in frontend/app/(protected)/layout.tsx
- [X] T031 [US1] Add auth API methods (signup, login, logout) to API client in frontend/lib/api.ts

**Checkpoint**: User Story 1 complete. Users can create accounts, log in, and log out. Protected routes redirect unauthenticated users.

---

## Phase 4: User Story 2 - View Task Dashboard (Priority: P2)

**Goal**: Display all tasks in a clean, responsive interface with cards on mobile and table on desktop

**Independent Test**: Log in, navigate to dashboard, verify tasks display correctly on mobile (cards) and desktop (table). Verify empty state and loading skeletons.

### Implementation for User Story 2

- [X] T032 [US2] Create useTasks hook with list query using React Query in frontend/hooks/useTasks.ts
- [X] T033 [US2] Add tasks.list method to API client in frontend/lib/api.ts
- [X] T034 [P] [US2] Create EmptyState component with friendly message and illustration in frontend/components/EmptyState.tsx
- [X] T035 [P] [US2] Create TaskCard component for mobile view with status indicator in frontend/components/TaskCard.tsx
- [X] T036 [P] [US2] Create TaskTable component for desktop view in frontend/components/TaskTable.tsx
- [X] T037 [US2] Create TaskList component orchestrating cards/table based on viewport in frontend/components/TaskList.tsx
- [X] T038 [US2] Create dashboard page integrating TaskList in frontend/app/(protected)/dashboard/page.tsx
- [X] T039 [US2] Create dashboard loading skeleton in frontend/app/(protected)/dashboard/loading.tsx
- [X] T040 [US2] Create dashboard error boundary with reset in frontend/app/(protected)/dashboard/error.tsx

**Checkpoint**: User Story 2 complete. Dashboard displays tasks responsively. Empty state and loading states work correctly.

---

## Phase 5: User Story 3 - Create New Task (Priority: P3)

**Goal**: Allow users to create new tasks with title (required) and description (optional) using optimistic updates

**Independent Test**: Click Add Task, enter title, submit. Verify task appears immediately in list with success toast.

### Implementation for User Story 3

- [X] T041 [US3] Create TaskModal component for create/edit forms in frontend/components/TaskModal.tsx
- [X] T042 [US3] Add tasks.create method to API client in frontend/lib/api.ts
- [X] T043 [US3] Add useCreateTask mutation with optimistic update to useTasks hook in frontend/hooks/useTasks.ts
- [X] T044 [US3] Wire up create task button and modal in dashboard page in frontend/app/(protected)/dashboard/page.tsx
- [X] T045 [US3] Add success/error toasts for task creation in frontend/hooks/useTasks.ts

**Checkpoint**: User Story 3 complete. Users can create tasks with optimistic updates and toast feedback.

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P4)

**Goal**: Allow users to edit task title and description with validation

**Independent Test**: Click edit on task, modify title/description, save. Verify changes persist with success toast.

### Implementation for User Story 4

- [X] T046 [US4] Add edit mode handling to TaskModal component in frontend/components/TaskModal.tsx
- [X] T047 [US4] Add tasks.update method to API client in frontend/lib/api.ts
- [X] T048 [US4] Add useUpdateTask mutation with optimistic update to useTasks hook in frontend/hooks/useTasks.ts
- [X] T049 [US4] Wire up edit button in TaskCard with modal trigger in frontend/components/TaskCard.tsx
- [X] T050 [US4] Wire up edit button in TaskTable with modal trigger in frontend/components/TaskTable.tsx

**Checkpoint**: User Story 4 complete. Users can edit tasks with optimistic updates and validation.

---

## Phase 7: User Story 5 - Toggle Task Completion (Priority: P5)

**Goal**: Allow users to mark tasks complete/incomplete with immediate visual feedback

**Independent Test**: Click checkbox on task. Verify immediate visual toggle with rollback on error.

### Implementation for User Story 5

- [X] T051 [US5] Add useToggleTask mutation with optimistic update to useTasks hook in frontend/hooks/useTasks.ts
- [X] T052 [US5] Wire up toggle handler in TaskCard component in frontend/components/TaskCard.tsx
- [X] T053 [US5] Wire up toggle handler in TaskTable component in frontend/components/TaskTable.tsx
- [X] T054 [US5] Add visual styling for completed tasks (strikethrough, muted) in frontend/components/TaskCard.tsx
- [X] T055 [US5] Add visual styling for completed tasks in table view in frontend/components/TaskTable.tsx

**Checkpoint**: User Story 5 complete. Task completion toggles instantly with visual feedback and rollback on failure.

---

## Phase 8: User Story 6 - Delete Task (Priority: P6)

**Goal**: Allow users to delete tasks with confirmation dialog

**Independent Test**: Click delete, confirm in dialog. Verify task removed from list with success toast.

### Implementation for User Story 6

- [X] T056 [US6] Create ConfirmDialog component for destructive actions in frontend/components/ConfirmDialog.tsx
- [X] T057 [US6] Add tasks.delete method to API client in frontend/lib/api.ts
- [X] T058 [US6] Add useDeleteTask mutation with optimistic update to useTasks hook in frontend/hooks/useTasks.ts
- [X] T059 [US6] Wire up delete button and confirm dialog in TaskCard in frontend/components/TaskCard.tsx
- [X] T060 [US6] Wire up delete button and confirm dialog in TaskTable in frontend/components/TaskTable.tsx

**Checkpoint**: User Story 6 complete. Users can delete tasks with confirmation and optimistic removal.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T061 Verify all toasts display correctly for success/error states across all operations
- [X] T062 Verify all loading states (buttons, forms, list) display correctly
- [X] T063 Verify dark mode works correctly across all components
- [X] T064 Verify responsive design: mobile cards, desktop table at 768px breakpoint
- [X] T065 Verify error boundaries catch and display friendly messages
- [X] T066 Verify 401 responses redirect to login with session expired message
- [ ] T067 Run quickstart.md validation - full signup → dashboard → CRUD flow (requires backend)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational (Phase 2) completion
  - US1 (P3) must complete before US2-US6 (auth required)
  - US2 (P4) can start after US1 (need dashboard to see tasks)
  - US3-US6 (P5-P8) can proceed in parallel after US2 (all need task list)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

```
US1 (Auth) → US2 (Dashboard) → US3 (Create) → US4 (Update)
                             ↘           ↘
                               US5 (Toggle)
                             ↘
                               US6 (Delete)
```

- **User Story 1**: No dependencies - gateway to all other stories
- **User Story 2**: Depends on US1 (need auth to view dashboard)
- **User Story 3**: Depends on US2 (need dashboard to show created tasks)
- **User Story 4**: Depends on US3 (need existing tasks to edit)
- **User Story 5**: Depends on US2 (need task list for toggle)
- **User Story 6**: Depends on US2 (need task list for delete)

### Within Each User Story

- Services/hooks before UI components
- API methods before mutations
- Base components before page integration
- Modal/dialog before wiring

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T003, T004 can run in parallel
T006, T007, T008 can run in parallel
```

**Phase 2 (Foundational)**:
```
T011, T012, T013 can run in parallel
T016, T017 can run in parallel
T018, T019, T020, T021, T022, T023 can run in parallel
```

**Phase 3 (US1 - Auth)**:
```
T026, T027 can run in parallel (login and signup pages)
```

**Phase 4 (US2 - Dashboard)**:
```
T034, T035, T036 can run in parallel
```

**Phase 6-8 (US4, US5, US6)**:
```
These entire phases can run in parallel once US3 is complete
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (Dashboard)
5. **STOP and VALIDATE**: Test auth flow and task viewing
6. Deploy/demo if ready - users can login and view tasks

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Test independently → Users can login
3. Add US2 (Dashboard) → Test independently → Users can view tasks
4. Add US3 (Create) → Test independently → Users can add tasks
5. Add US4-US6 → Test independently → Full CRUD complete
6. Polish → Production ready

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2)**

This delivers:
- Full authentication flow
- Task viewing with responsive design
- Loading states and error handling

---

## Summary

| Phase | Tasks | User Story | Parallel Opportunities |
|-------|-------|------------|------------------------|
| Phase 1: Setup | T001-T008 (8) | N/A | 5 parallel groups |
| Phase 2: Foundational | T009-T023 (15) | N/A | 6 parallel groups |
| Phase 3: US1 Auth | T024-T031 (8) | P1 | 2 parallel pairs |
| Phase 4: US2 Dashboard | T032-T040 (9) | P2 | 3 parallel groups |
| Phase 5: US3 Create | T041-T045 (5) | P3 | Sequential |
| Phase 6: US4 Update | T046-T050 (5) | P4 | 2 parallel pairs |
| Phase 7: US5 Toggle | T051-T055 (5) | P5 | 2 parallel pairs |
| Phase 8: US6 Delete | T056-T060 (5) | P6 | 2 parallel pairs |
| Phase 9: Polish | T061-T067 (7) | N/A | Sequential |
| **TOTAL** | **67 tasks** | **6 stories** | **~22 parallel** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
