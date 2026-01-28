# Feature Specification: AI-Powered Todo Chatbot Integration

**Feature Branch**: `002-ai-todo-chatbot`
**Created**: 2025-01-16
**Status**: Draft
**Input**: Phase III chatbot integration extending Phase II backend

## Overview

Extend the Phase II full-stack Todo application (Next.js frontend + FastAPI backend with Neon DB & Better Auth JWT) to add a conversational AI chatbot that manages Todo tasks via natural language. Users can interact with a floating chat interface to add, list, complete, update, and delete tasks using everyday language in English or Urdu.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task via Chat (Priority: P1)

As a logged-in user, I want to add a new task by typing a natural language message like "Add buy groceries to my list" so that I can quickly capture tasks without navigating forms.

**Why this priority**: Core chatbot functionality - if users cannot add tasks via chat, the feature has no value.

**Independent Test**: User sends "Add buy milk", receives confirmation "Task 'buy milk' added!", and sees the task appear in their dashboard task list.

**Acceptance Scenarios**:

1. **Given** user is logged in with valid JWT, **When** user types "Add buy groceries", **Then** chatbot creates task and responds with confirmation including task title
2. **Given** user is logged in, **When** user types "میری لسٹ میں دودھ خریدنا شامل کریں" (Urdu: add buy milk to my list), **Then** chatbot creates task and responds in Urdu with confirmation
3. **Given** user is logged in, **When** user types "Add task with very long description exceeding normal limits", **Then** chatbot creates task and truncates if needed, confirming the action

---

### User Story 2 - List Tasks via Chat (Priority: P1)

As a logged-in user, I want to ask the chatbot to show my tasks by typing "Show my tasks" so that I can quickly review what needs to be done.

**Why this priority**: Users need to see their tasks to interact meaningfully with the chatbot.

**Independent Test**: User sends "Show my tasks", receives formatted list of their pending tasks with titles and status.

**Acceptance Scenarios**:

1. **Given** user has 3 pending tasks, **When** user types "Show my tasks", **Then** chatbot lists all 3 tasks with titles and status
2. **Given** user has no tasks, **When** user types "What's on my list?", **Then** chatbot responds "You have no tasks yet!"
3. **Given** user types "میرے کام دکھائیں" (Urdu: show my tasks), **When** user has tasks, **Then** chatbot lists tasks with Urdu response

---

### User Story 3 - Complete Task via Chat (Priority: P2)

As a logged-in user, I want to mark a task complete by saying "Complete task 5" or "Mark buy groceries as done" so that I can update task status conversationally.

**Why this priority**: Completing tasks is essential for todo workflow but depends on listing/adding first.

**Independent Test**: User sends "Complete task 1", task status changes to completed, chatbot confirms "Task 'buy groceries' marked complete!"

**Acceptance Scenarios**:

1. **Given** user has task with ID 5 titled "Buy milk", **When** user types "Complete task 5", **Then** task status changes to completed and chatbot confirms with task title
2. **Given** user has a task titled "Exercise", **When** user types "Mark exercise as done", **Then** chatbot finds task by title and completes it
3. **Given** user tries to complete non-existent task ID 999, **When** user types "Complete task 999", **Then** chatbot responds "Task not found"

---

### User Story 4 - Delete Task via Chat (Priority: P2)

As a logged-in user, I want to delete a task by saying "Delete task 3" so that I can remove unwanted items from my list.

**Why this priority**: Users need to clean up completed or irrelevant tasks.

**Independent Test**: User sends "Delete task 1", task is removed from database, chatbot confirms "Task 'buy groceries' deleted!"

**Acceptance Scenarios**:

1. **Given** user has task with ID 3, **When** user types "Delete task 3", **Then** task is deleted and chatbot confirms deletion
2. **Given** user tries to delete another user's task, **When** request is made, **Then** chatbot responds "Task not found" (user isolation enforced)
3. **Given** user types "Remove everything", **When** processed, **Then** chatbot asks for confirmation before bulk delete

---

### User Story 5 - Update Task via Chat (Priority: P3)

As a logged-in user, I want to update a task's title or description by saying "Update task 2 title to Buy organic milk" so that I can modify existing tasks.

**Why this priority**: Nice-to-have refinement capability, lower priority than core CRUD.

**Independent Test**: User sends "Change task 2 title to Updated Title", task title changes, chatbot confirms.

**Acceptance Scenarios**:

1. **Given** user has task with ID 2, **When** user types "Update task 2 title to New Title", **Then** task title updates and chatbot confirms
2. **Given** user has task with ID 2, **When** user types "Change description of task 2 to New description here", **Then** task description updates

---

### User Story 6 - Conversation History Persistence (Priority: P2)

As a logged-in user, I want my chat conversations to persist across browser sessions so that I can refer back to previous interactions.

**Why this priority**: Important for user experience and continuity across sessions.

**Independent Test**: User closes browser, reopens, and sees previous chat messages in the conversation window.

**Acceptance Scenarios**:

1. **Given** user has previous chat history, **When** user returns to dashboard, **Then** previous conversations are loaded from database
2. **Given** user starts new conversation, **When** no conversation_id provided, **Then** new conversation is created with unique ID
3. **Given** user has conversation_id, **When** user sends message, **Then** message is appended to existing conversation

---

### User Story 7 - Chatbot Icon and Interface (Priority: P1)

As a logged-in user, I want a floating chat icon on my dashboard that opens a chat interface when clicked so that I can easily access the chatbot.

**Why this priority**: Entry point to all chatbot functionality - without visible UI, feature is unusable.

**Independent Test**: User sees chat icon on dashboard, clicks it, chat panel opens with input field and send button.

**Acceptance Scenarios**:

1. **Given** user is on dashboard, **When** page loads, **Then** floating chat icon appears in bottom-right corner
2. **Given** chat icon is visible, **When** user clicks icon, **Then** ChatKit UI opens as modal or sidebar
3. **Given** chat is open, **When** user types message and clicks send, **Then** message appears in chat with loading indicator until response

---

### Edge Cases

- What happens when Cohere API is unavailable? Chatbot responds with friendly error message: "I'm having trouble connecting. Please try again in a moment."
- What happens when user sends empty message? Chatbot ignores or prompts "Please type a message."
- What happens when JWT expires mid-conversation? Chat endpoint returns 401, frontend redirects to login.
- What happens when database connection fails? Chatbot responds with graceful error, logs incident.
- What happens when user sends very long message (>10000 chars)? Message is truncated with warning.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide stateless POST `/api/{user_id}/chat` endpoint accepting `{ message: string, conversation_id?: number }`
- **FR-002**: System MUST return `{ conversation_id: number, response: string, tool_calls: array }` from chat endpoint
- **FR-003**: System MUST validate JWT token on every chat request using Phase II Better Auth
- **FR-004**: System MUST expose 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- **FR-005**: Each MCP tool MUST filter operations by authenticated user_id (user isolation)
- **FR-006**: System MUST persist conversations and messages in Neon DB with Conversation and Message models
- **FR-007**: System MUST use Cohere API key for all LLM reasoning (not OpenAI/Gemini)
- **FR-008**: System MUST detect Urdu script in user messages and respond in Urdu when detected
- **FR-009**: Frontend MUST display floating chat icon on dashboard (bottom-right position)
- **FR-010**: Frontend MUST open ChatKit UI when chat icon is clicked
- **FR-011**: ChatKit MUST send requests to backend with JWT authorization header
- **FR-012**: Chat interface MUST show loading state while awaiting response
- **FR-013**: Server MUST be stateless - no in-memory conversation storage between requests
- **FR-014**: MCP tools MUST reuse Phase II SQLModel Task model and database session

### Key Entities

- **Conversation**: Represents a chat session. Attributes: id, user_id, created_at, updated_at. User can have multiple conversations.
- **Message**: Represents a single message in a conversation. Attributes: id, conversation_id, user_id, role (user/assistant), content, tool_calls (optional JSON), created_at. Belongs to one Conversation.
- **Task** (existing from Phase II): Todo item. Attributes: id, user_id, title, description, status, created_at, updated_at.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task via natural language chat within 5 seconds of sending message
- **SC-002**: Users can list all their tasks by typing "show my tasks" and receive response within 3 seconds
- **SC-003**: Users can complete, delete, or update tasks via chat commands with immediate visual confirmation
- **SC-004**: Conversation history persists and is available when user returns within 24 hours
- **SC-005**: User can only see and modify their own tasks (100% user isolation)
- **SC-006**: Urdu messages receive Urdu responses with same functionality as English
- **SC-007**: Chat interface is accessible within 1 click from any dashboard page
- **SC-008**: System gracefully handles errors with user-friendly messages (no technical stack traces)
- **SC-009**: System remains responsive under normal usage (single user testing scenarios)

## Assumptions

- Phase II backend (FastAPI, Neon DB, Better Auth JWT) is fully functional and deployed
- Phase II Task model and authentication endpoints are stable and unchanged
- Cohere API key is valid and has sufficient quota for development/testing
- OpenAI Agents SDK is compatible with Cohere as LLM provider
- OpenAI ChatKit UI is available and properly licensed for use
- Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Network connectivity is stable during chat interactions
- Single-user testing is sufficient for initial validation (no load testing required)

## Dependencies

- Phase II Backend: FastAPI with existing `/api/tasks` CRUD endpoints
- Phase II Frontend: Next.js dashboard with authentication flows
- Phase II Database: Neon PostgreSQL with existing User and Task tables
- Phase II Auth: Better Auth JWT tokens for authentication
- External: Cohere API for LLM reasoning
- External: OpenAI Agents SDK for agent orchestration
- External: MCP SDK for tool definition and execution
- External: OpenAI ChatKit UI components for frontend

## Out of Scope

- Voice input/output (stretch goal for future phase)
- Multi-user real-time collaboration
- Task sharing between users
- Push notifications for task reminders
- Mobile app (web-only for Phase III)
- Performance optimization for high-concurrency scenarios
- Advanced NLP for complex queries (e.g., "show tasks from last week")
