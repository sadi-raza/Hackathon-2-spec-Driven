# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/002-ai-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Tests are NOT explicitly requested. Tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source, `backend/tests/` for tests
- **Frontend**: `frontend/` for Next.js source

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Add Phase III dependencies and configuration

- [x] T001 Add Cohere SDK dependency to backend/requirements.txt
- [x] T002 [P] Add OpenAI Agents SDK dependency to backend/requirements.txt
- [x] T003 [P] Add MCP SDK dependency to backend/requirements.txt
- [x] T004 [P] Add COHERE_API_KEY to backend/.env.example
- [x] T005 [P] Add @assistant-ui/react package to frontend/package.json
- [x] T006 [P] Add NEXT_PUBLIC_CHATBOT_ENABLED to frontend/.env.example
- [x] T007 Create backend/app/mcp/__init__.py directory structure
- [x] T008 [P] Create backend/app/agent/__init__.py directory structure
- [x] T009 [P] Create backend/app/utils/__init__.py directory structure
- [x] T010 [P] Create frontend/components/chat/ directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create Conversation model in backend/app/models/conversation.py
- [x] T012 [P] Create Message model in backend/app/models/message.py
- [x] T013 Update backend/app/models/__init__.py to export Conversation and Message
- [x] T014 Add conversations relationship to User model in backend/app/models/user.py
- [x] T015 Create ChatRequest and ChatResponse schemas in backend/app/schemas/chat.py
- [x] T016 [P] Create ConversationSchema and MessageSchema in backend/app/schemas/conversation.py
- [x] T017 Update backend/app/schemas/__init__.py to export new schemas
- [x] T018 Create ConversationService in backend/app/services/conversation_service.py
- [x] T019 Create CohereModel wrapper in backend/app/agent/cohere_model.py
- [x] T020 [P] Create Urdu detection utility in backend/app/utils/urdu.py
- [x] T021 Install new dependencies: pip install cohere mcp openai-agents
- [x] T022 [P] Install frontend dependencies: npm install @assistant-ui/react

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 7 - Chatbot Icon and Interface (Priority: P1)

**Goal**: Add floating chat icon to dashboard that opens ChatKit UI

**Independent Test**: User sees chat icon, clicks it, chat panel opens

**Why first**: This is the entry point - without UI, no other stories can be tested manually

### Implementation for User Story 7

- [x] T023 [P] [US7] Create ChatIcon component in frontend/components/chat/ChatIcon.tsx
- [x] T024 [P] [US7] Create ChatModal component in frontend/components/chat/ChatModal.tsx
- [x] T025 [US7] Create chat API client in frontend/lib/chat-api.ts
- [x] T026 [US7] Create ChatMessages display component in frontend/components/chat/ChatMessages.tsx
- [x] T027 [US7] Create chat components index in frontend/components/chat/index.ts
- [x] T028 [US7] Add ChatIcon to dashboard layout in frontend/app/(protected)/dashboard/page.tsx
- [x] T029 [US7] Add loading state component for chat in frontend/components/chat/ChatLoading.tsx

**Checkpoint**: Chat UI visible and interactive (opens/closes), ready for backend integration

---

## Phase 4: User Story 1 - Add Task via Chat (Priority: P1)

**Goal**: User can add a task by typing natural language like "Add buy groceries"

**Independent Test**: Send "Add buy milk", see confirmation, task appears in list

### Implementation for User Story 1

- [x] T030 [US1] Create add_task MCP tool in backend/app/mcp/tools.py
- [x] T031 [US1] Create MCP server registration in backend/app/mcp/__init__.py
- [x] T032 [US1] Create TodoAgent with add_task capability in backend/app/agent/todo_agent.py
- [x] T033 [US1] Create ChatService for orchestration in backend/app/services/chat_service.py
- [x] T034 [US1] Create chat router with POST endpoint in backend/app/api/chat.py
- [x] T035 [US1] Register chat router in backend/app/main.py (or app __init__)
- [x] T036 [US1] Connect ChatModal to backend /api/{user_id}/chat endpoint
- [x] T037 [US1] Add confirmation message formatting in chat response

**Checkpoint**: Can add tasks via chat, see confirmation

---

## Phase 5: User Story 2 - List Tasks via Chat (Priority: P1)

**Goal**: User can list tasks by typing "Show my tasks"

**Independent Test**: Send "Show my tasks", see formatted list of tasks

### Implementation for User Story 2

- [x] T038 [US2] Add list_tasks MCP tool in backend/app/mcp/tools.py
- [x] T039 [US2] Add list_tasks to TodoAgent tools in backend/app/agent/todo_agent.py
- [x] T040 [US2] Format task list response in ChatService
- [x] T041 [US2] Display task list in ChatMessages component

**Checkpoint**: Can list tasks via chat

---

## Phase 6: User Story 3 - Complete Task via Chat (Priority: P2)

**Goal**: User can mark task complete by saying "Complete task 5"

**Independent Test**: Send "Complete task 1", status changes, confirmation shown

### Implementation for User Story 3

- [x] T042 [US3] Add complete_task MCP tool in backend/app/mcp/tools.py
- [x] T043 [US3] Add complete_task to TodoAgent tools in backend/app/agent/todo_agent.py
- [x] T044 [US3] Handle task-not-found error gracefully

**Checkpoint**: Can complete tasks via chat

---

## Phase 7: User Story 4 - Delete Task via Chat (Priority: P2)

**Goal**: User can delete task by saying "Delete task 3"

**Independent Test**: Send "Delete task 1", task removed, confirmation shown

### Implementation for User Story 4

- [x] T045 [US4] Add delete_task MCP tool in backend/app/mcp/tools.py
- [x] T046 [US4] Add delete_task to TodoAgent tools in backend/app/agent/todo_agent.py
- [x] T047 [US4] Handle bulk delete confirmation request

**Checkpoint**: Can delete tasks via chat

---

## Phase 8: User Story 6 - Conversation History Persistence (Priority: P2)

**Goal**: Chat history persists across sessions

**Independent Test**: Close browser, reopen, see previous messages

### Implementation for User Story 6

- [x] T048 [US6] Save user messages in ConversationService
- [x] T049 [US6] Save assistant responses in ConversationService
- [x] T050 [US6] Load conversation history on chat open in ChatService
- [x] T051 [US6] Create GET /api/{user_id}/conversations endpoint in backend/app/api/conversations.py
- [x] T052 [US6] Create GET /api/{user_id}/conversations/{id} endpoint
- [x] T053 [US6] Register conversations router in backend/app/main.py
- [x] T054 [US6] Load previous messages in ChatModal on mount
- [x] T055 [US6] Display tool_calls in ChatMessages component

**Checkpoint**: Conversations persist across page refreshes

---

## Phase 9: User Story 5 - Update Task via Chat (Priority: P3)

**Goal**: User can update task by saying "Update task 2 title to New Title"

**Independent Test**: Send update command, task updated, confirmation shown

### Implementation for User Story 5

- [x] T056 [US5] Add update_task MCP tool in backend/app/mcp/tools.py
- [x] T057 [US5] Add update_task to TodoAgent tools in backend/app/agent/todo_agent.py
- [x] T058 [US5] Parse update parameters (title, description) from natural language

**Checkpoint**: Can update tasks via chat

---

## Phase 10: Bonus - Urdu Support (+100 points)

**Goal**: Detect Urdu messages and respond in Urdu

**Independent Test**: Send "میری لسٹ میں دودھ خریدنا شامل کریں", get Urdu response

### Implementation for Urdu Support

- [x] T059 [URDU] Implement Urdu detection in backend/app/utils/urdu.py
- [x] T060 [URDU] Add Urdu detection to ChatService before agent call
- [x] T061 [URDU] Add Urdu response instruction to agent system prompt
- [x] T062 [URDU] Create Urdu confirmation templates in confirmation-responder skill

**Checkpoint**: Urdu messages get Urdu responses

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and error handling

- [x] T063 Add graceful error handling for Cohere API failures in ChatService
- [x] T064 [P] Add graceful error handling for database failures
- [x] T065 [P] Add request validation and sanitization to chat endpoint
- [x] T066 Add loading state animation to ChatModal
- [x] T067 [P] Add empty state message when no conversation history
- [x] T068 Run quickstart.md verification steps
- [x] T069 [P] Update README.md with Phase III chatbot instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US7 (Chat UI) should complete first for manual testing
  - US1, US2 can proceed after US7
  - US3, US4, US6 can proceed after US1/US2
  - US5 can proceed after US3
  - Urdu can proceed after US1
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 2 (Foundation)
      │
      ▼
Phase 3 (US7: Chat UI) ──────────────────────┐
      │                                       │
      ├──────────────┬───────────────┐        │
      ▼              ▼               ▼        │
Phase 4 (US1)   Phase 5 (US2)   [Frontend works]
      │              │
      ├──────────────┼───────────────┐
      ▼              ▼               ▼
Phase 6 (US3)   Phase 7 (US4)   Phase 8 (US6)
      │
      ▼
Phase 9 (US5)
      │
      ├─────────────────────────────────────────
      ▼
Phase 10 (Urdu) ── can start after US1 is complete
      │
      ▼
Phase 11 (Polish)
```

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend integration
- Core implementation before error handling

### Parallel Opportunities

**Phase 1 (Setup)**: T002-T010 can run in parallel
**Phase 2 (Foundation)**: T011-T012, T015-T016, T019-T020, T021-T022 can run in parallel
**Phase 3 (US7)**: T023-T024 can run in parallel
**Phase 11 (Polish)**: T064-T065, T067, T069 can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch model creation in parallel:
Task T011: "Create Conversation model in backend/app/models/conversation.py"
Task T012: "Create Message model in backend/app/models/message.py"

# Then launch schema creation in parallel:
Task T015: "Create ChatRequest and ChatResponse schemas in backend/app/schemas/chat.py"
Task T016: "Create ConversationSchema and MessageSchema in backend/app/schemas/conversation.py"
```

---

## Implementation Strategy

### MVP First (User Stories 7 + 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US7 (Chat UI)
4. Complete Phase 4: US1 (Add Task)
5. Complete Phase 5: US2 (List Tasks)
6. **STOP and VALIDATE**: Test add/list via chat
7. Demo-ready with core functionality

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US7 (Chat UI) → UI visible → Demo point
3. Add US1 (Add Task) → Can add via chat → Demo point
4. Add US2 (List Tasks) → Can list via chat → Demo point
5. Add US3, US4, US6 → Full CRUD via chat
6. Add US5 → Update capability
7. Add Urdu → Bonus points
8. Polish → Production ready

### Single Developer Strategy

Follow phases in order:
1. Setup (1 hour)
2. Foundational (2 hours)
3. US7 - Chat UI (1 hour)
4. US1 - Add Task (2 hours)
5. US2 - List Tasks (1 hour)
6. US3 - Complete Task (1 hour)
7. US4 - Delete Task (1 hour)
8. US6 - Persistence (2 hours)
9. US5 - Update Task (1 hour)
10. Urdu Bonus (1 hour)
11. Polish (1 hour)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

| Phase | Story | Tasks | Parallel |
|-------|-------|-------|----------|
| 1. Setup | - | 10 | 9 |
| 2. Foundational | - | 12 | 8 |
| 3. Chat UI | US7 | 7 | 2 |
| 4. Add Task | US1 | 8 | 0 |
| 5. List Tasks | US2 | 4 | 0 |
| 6. Complete Task | US3 | 3 | 0 |
| 7. Delete Task | US4 | 3 | 0 |
| 8. Persistence | US6 | 8 | 0 |
| 9. Update Task | US5 | 3 | 0 |
| 10. Urdu | URDU | 4 | 0 |
| 11. Polish | - | 7 | 4 |
| **TOTAL** | | **69** | **23** |

**MVP Scope**: Phases 1-5 (US7 + US1 + US2) = 41 tasks
**Full Scope**: All phases = 69 tasks
