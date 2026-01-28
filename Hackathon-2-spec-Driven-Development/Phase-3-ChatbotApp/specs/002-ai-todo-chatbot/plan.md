# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `002-ai-todo-chatbot` | **Date**: 2025-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ai-todo-chatbot/spec.md`

## Summary

Extend the Phase II full-stack Todo application with an AI-powered chatbot that manages tasks via natural language. The chatbot uses Cohere API for LLM reasoning, OpenAI Agents SDK for orchestration, and MCP SDK for tool execution. All components are stateless with conversation persistence in Neon DB.

---

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/Next.js 14 (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Cohere SDK, OpenAI Agents SDK, MCP SDK, ChatKit
**Storage**: Neon PostgreSQL (existing) + new Conversation/Message tables
**Testing**: pytest (backend), manual UI testing (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (monorepo with backend/ and frontend/)
**Performance Goals**: <5s response time for chat messages
**Constraints**: Stateless design, Cohere-only LLM, user isolation
**Scale/Scope**: Single user testing, demo-ready

---

## Constitution Check

*GATE: All checks PASSED*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Zero Manual Coding | ✅ PASS | All code Claude-generated |
| II. Spec-Driven Development | ✅ PASS | spec.md → plan.md → tasks.md |
| III. Reusable Intelligence | ✅ PASS | Using 8+ agents/skills |
| IV. Phase III Requirements | ✅ PASS | Extending Phase II, 5 MCP tools |
| V. Environment Variables | ✅ PASS | COHERE_API_KEY, env-based secrets |
| VI. Security & Auth | ✅ PASS | Reusing Phase II JWT |
| VII. Stateless Design | ✅ PASS | DB-backed state only |
| VIII. Monorepo Structure | ✅ PASS | backend/, frontend/, specs/ |
| IX. Bonus Features | ✅ PASS | Urdu support included |
| X. Deliverables | ✅ PASS | Clean commits with Task IDs |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-todo-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technical research decisions
├── data-model.md        # Conversation + Message models
├── quickstart.md        # Setup and verification guide
├── contracts/
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.md     # MCP tool signatures
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (sp.tasks output)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── task.py           # Existing - no changes
│   │   ├── user.py           # Existing - add relationship
│   │   ├── conversation.py   # NEW: Conversation model
│   │   └── message.py        # NEW: Message model
│   ├── schemas/
│   │   ├── chat.py           # NEW: Chat request/response schemas
│   │   └── conversation.py   # NEW: Conversation schemas
│   ├── services/
│   │   ├── task_service.py   # Existing - no changes
│   │   ├── chat_service.py   # NEW: Chat orchestration
│   │   └── conversation_service.py  # NEW: Conversation CRUD
│   ├── mcp/
│   │   ├── __init__.py       # NEW: MCP server setup
│   │   └── tools.py          # NEW: 5 MCP tools
│   ├── agent/
│   │   ├── __init__.py       # NEW: Agent setup
│   │   ├── cohere_model.py   # NEW: Cohere model wrapper
│   │   └── todo_agent.py     # NEW: Agent with tools
│   ├── api/
│   │   ├── tasks.py          # Existing - no changes
│   │   ├── chat.py           # NEW: Chat endpoint
│   │   └── conversations.py  # NEW: Conversation endpoints
│   └── utils/
│       └── urdu.py           # NEW: Urdu detection
└── tests/
    ├── test_chat.py          # NEW: Chat endpoint tests
    └── test_mcp_tools.py     # NEW: MCP tool tests

frontend/
├── app/
│   └── (protected)/
│       └── dashboard/
│           └── page.tsx      # MODIFY: Add chat components
├── components/
│   ├── chat/
│   │   ├── ChatIcon.tsx      # NEW: Floating chat icon
│   │   ├── ChatModal.tsx     # NEW: Chat modal/sidebar
│   │   └── ChatMessages.tsx  # NEW: Message display
│   └── ...
└── lib/
    └── chat-api.ts           # NEW: Chat API client
```

**Structure Decision**: Web application pattern (Option 2) - extending existing backend/ and frontend/ directories.

---

## High-Level Architecture

### Request Flow (Stateless)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│  /api/chat  │────▶│  Chat Svc   │
│  (ChatKit)  │     │  (FastAPI)  │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                           │                    │
                    ┌──────▼──────┐      ┌──────▼──────┐
                    │  JWT Auth   │      │    Agent    │
                    │ Middleware  │      │  (Cohere)   │
                    └─────────────┘      └──────┬──────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │                           │                           │
             ┌──────▼──────┐            ┌───────▼───────┐           ┌───────▼───────┐
             │  MCP Tools  │            │ Conversation  │           │    Neon DB    │
             │ (5 actions) │            │  Persistence  │           │   (state)     │
             └─────────────┘            └───────────────┘           └───────────────┘
```

### Component Responsibilities

1. **ChatKit Frontend**: UI components, message display, send button
2. **Chat Endpoint**: JWT validation, request parsing, response formatting
3. **Chat Service**: Orchestrates agent, persists messages
4. **Cohere Agent**: LLM reasoning, intent parsing, tool selection
5. **MCP Tools**: Task CRUD operations with user isolation
6. **Conversation Service**: Create/fetch conversations and messages
7. **Neon DB**: Persistent storage for all state

---

## 1. High-Level Architecture

### Extending Phase II FastAPI Backend

- Add new routers: `/api/{user_id}/chat`, `/api/{user_id}/conversations`
- Reuse existing: JWT middleware, database session, Task model
- New models: Conversation, Message (see data-model.md)
- New services: ChatService, ConversationService
- MCP tools registered at app startup

### Cohere API Integration

```python
# backend/app/agent/cohere_model.py
import cohere
from openai_agents import Model

class CohereModel(Model):
    def __init__(self):
        self.client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

    async def generate(self, messages, tools=None):
        response = await self.client.chat(
            model="command-r-plus",
            messages=self._convert_messages(messages),
            tools=self._convert_tools(tools) if tools else None
        )
        return self._convert_response(response)
```

### Stateless Flow

1. Request arrives with JWT + message + optional conversation_id
2. Validate JWT, extract user_id
3. Fetch conversation history from DB (if conversation_id provided)
4. Build agent context with history
5. Run agent with Cohere LLM
6. Store user message + assistant response in DB
7. Return response (new messages not stored in memory)

---

## 2. Database Extensions

See [data-model.md](./data-model.md) for complete schema.

**New Tables**:
- `conversations`: id, user_id, title, created_at, updated_at
- `messages`: id, conversation_id, user_id, role, content, tool_calls, created_at

**Indexes**:
- `idx_conversations_user_id`
- `idx_messages_conversation`

**Relationships**:
- User → Conversations (one-to-many)
- Conversation → Messages (one-to-many, cascade delete)

---

## 3. MCP Server Implementation

See [contracts/mcp-tools.md](./contracts/mcp-tools.md) for complete signatures.

**5 Stateless Tools**:

| Tool | Parameters | Returns |
|------|------------|---------|
| add_task | user_id, title, description? | {task_id, status, title} |
| list_tasks | user_id, status? | {tasks[], total, filter} |
| complete_task | user_id, task_id | {task_id, status, title} |
| delete_task | user_id, task_id | {task_id, status, title} |
| update_task | user_id, task_id, title?, description? | {task_id, status, title} |

**User Isolation**: All tools filter by user_id from JWT.

---

## 4. Chat Endpoint

See [contracts/chat-api.yaml](./contracts/chat-api.yaml) for OpenAPI spec.

**POST /api/{user_id}/chat**

Request:
```json
{
  "message": "Add buy groceries to my list",
  "conversation_id": "optional-uuid"
}
```

Response:
```json
{
  "conversation_id": "uuid",
  "response": "Task 'buy groceries' added!",
  "tool_calls": [...]
}
```

---

## 5. Agent Logic

### Cohere as LLM Backend

- Model: `command-r-plus` via Cohere API
- Wrapper: Custom `CohereModel` class for OpenAI Agents SDK
- All LLM calls use COHERE_API_KEY (Constitution V)

### Intent Parsing

1. Agent receives user message + conversation history
2. LLM determines intent (add, list, complete, delete, update)
3. Extracts parameters (task title, ID, status filter)
4. Calls appropriate MCP tool(s)

### Tool Chaining

Example: "Show my tasks and complete the first one"
1. Agent calls `list_tasks(user_id)`
2. Receives task list
3. Identifies first task ID
4. Calls `complete_task(user_id, first_task_id)`
5. Returns combined response

### Confirmation + Error Handling

- Success: "Task 'buy groceries' added!"
- Not found: "I couldn't find that task."
- Error: "Something went wrong. Please try again."

---

## 6. Frontend Integration

### Floating Chat Icon

- Position: bottom-right corner of dashboard
- Icon: MessageCircle from lucide-react
- Click: Opens ChatKit modal/sidebar

### ChatKit UI Setup

```tsx
// components/chat/ChatModal.tsx
import { Chat } from '@openai/chatkit';

export function ChatModal({ userId, token }) {
  return (
    <Chat
      apiUrl={`${API_BASE}/api/${userId}/chat`}
      headers={{ Authorization: `Bearer ${token}` }}
      placeholder="Type a message..."
    />
  );
}
```

### Domain Configuration

- Development: localhost allowed by default
- Production: Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY in .env

---

## 7. Bonus: Urdu Detection

### Script Detection Logic

```python
# backend/app/utils/urdu.py
import re

URDU_PATTERN = re.compile(r'[\u0600-\u06FF]')

def detect_urdu(text: str) -> bool:
    """Detect if text contains Urdu/Arabic script."""
    return bool(URDU_PATTERN.search(text))
```

### Urdu Response Generation

When Urdu detected:
1. Add system message: "Respond in Urdu using the same script"
2. Agent generates Urdu response
3. Confirmations use Urdu equivalents

---

## 8. Testing & Verification

### Key Test Flows

1. **Add Task**: "Add buy groceries" → task created
2. **List Tasks**: "Show my tasks" → formatted list
3. **Complete Task**: "Complete task 1" → status updated
4. **Delete Task**: "Delete task 2" → task removed
5. **Update Task**: "Change task 1 to buy organic milk" → title updated

### Multi-Turn Conversation

1. Start conversation: "What's on my list?"
2. Continue: "Add milk"
3. Continue: "Mark it done"
4. Verify history persists in DB

### Error Cases

- Invalid JWT → 401
- Other user's task → 404
- Empty message → "Please type a message"
- Cohere API down → "Having trouble connecting"

### Urdu Test

- Input: "میری لسٹ میں دودھ خریدنا شامل کریں"
- Expected: Urdu confirmation, task created

---

## Agents & Skills Mapping

| Component | Agent | Skill |
|-----------|-------|-------|
| Request orchestration | @chatbot-orchestrator | - |
| Intent parsing | @agent-logic-master | natural-language-parser |
| MCP tools | @mcp-tool-builder | mcp-tool-craft |
| DB models | @conversation-persistence-expert | conversation-state-manager |
| Error handling | @agent-logic-master | error-graceful-handler |
| Frontend UI | @chatkit-frontend-integrator | - |
| Confirmations | - | confirmation-responder |
| DB operations | @database-genius | database-genius |

---

## Complexity Tracking

No constitution violations. Standard Phase III implementation.

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement in order: DB models → MCP tools → Agent → Chat endpoint → Frontend
3. Test each component before integration
4. Demo: Show natural language task management
