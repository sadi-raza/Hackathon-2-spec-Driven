# Phase 0 Research: AI-Powered Todo Chatbot

**Feature**: 002-ai-todo-chatbot
**Date**: 2025-01-16
**Status**: Complete

## Research Summary

All technical decisions resolved. No NEEDS CLARIFICATION items remaining.

---

## 1. Cohere API Integration with OpenAI Agents SDK

### Decision
Use Cohere's Chat API via custom model configuration in OpenAI Agents SDK.

### Rationale
- Constitution mandates Cohere API key for ALL LLM reasoning (Principle V)
- OpenAI Agents SDK supports custom model backends via `Model` class
- Cohere's command-r-plus model provides comparable quality to GPT-4

### Implementation Pattern
```python
from agents import Agent, Model
import cohere

# Create Cohere client
cohere_client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

# Create custom model wrapper for Agents SDK
class CohereModel(Model):
    async def generate(self, messages, tools=None):
        response = await cohere_client.chat(
            model="command-r-plus",
            messages=messages,
            tools=tools
        )
        return response
```

### Alternatives Considered
- **Direct OpenAI API**: Rejected - Constitution explicitly forbids
- **LiteLLM**: Adds complexity, direct Cohere integration simpler
- **LangChain**: Overkill for this use case

---

## 2. MCP SDK Integration Strategy

### Decision
Implement MCP tools as FastAPI routes with MCP SDK tool decorators inside the existing backend.

### Rationale
- Constitution requires MCP tools inside existing FastAPI backend
- Official MCP SDK provides `@tool` decorator for function-based tools
- Stateless design mandated - each tool call is independent

### Implementation Pattern
```python
from mcp import Tool, tool

@tool
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Add a new task for the user."""
    # Reuse existing TaskService
    task = await task_service.create_task(title, description, user_id)
    return {"task_id": task.id, "status": "created", "title": task.title}
```

### Alternatives Considered
- **Separate MCP server process**: Rejected - Constitution requires extending existing backend
- **REST-only approach**: Doesn't meet MCP SDK requirement

---

## 3. Conversation Persistence Design

### Decision
Two new SQLModel tables: `Conversation` and `Message` with user_id foreign key for isolation.

### Rationale
- Stateless design mandates DB-backed conversation state
- User isolation requires user_id on both tables
- Matches existing Phase II SQLModel pattern

### Schema Design
- `Conversation`: id (UUID), user_id (FK), created_at, updated_at
- `Message`: id (UUID), conversation_id (FK), user_id (FK), role (enum), content, tool_calls (JSON), created_at

### Alternatives Considered
- **Single messages table**: Loses conversation grouping
- **In-memory Redis**: Not stateless, adds infrastructure

---

## 4. ChatKit Frontend Integration

### Decision
Use OpenAI ChatKit React components with custom API adapter for our backend.

### Rationale
- ChatKit provides ready-made UI components (chat window, input, messages)
- Requires NEXT_PUBLIC_OPENAI_DOMAIN_KEY for production
- Will send requests to `/api/{user_id}/chat` with JWT header

### Implementation Pattern
```tsx
import { Chat } from '@openai/chatkit';

<Chat
  apiUrl={`/api/${userId}/chat`}
  headers={{ Authorization: `Bearer ${token}` }}
  onMessage={(msg) => handleMessage(msg)}
/>
```

### Alternatives Considered
- **Custom chat UI**: More work, less polished
- **Vercel AI SDK**: Good alternative, but ChatKit specified in spec

---

## 5. Urdu Language Detection

### Decision
Detect Urdu using Unicode script range check (U+0600-U+06FF for Arabic script).

### Rationale
- Urdu uses Arabic script with Unicode range 0600-06FF
- Simple regex check: `/[\u0600-\u06FF]/` on message content
- When detected, instruct agent to respond in Urdu

### Implementation Pattern
```python
import re

def detect_urdu(text: str) -> bool:
    """Detect if text contains Urdu/Arabic script."""
    return bool(re.search(r'[\u0600-\u06FF]', text))
```

### Alternatives Considered
- **Language detection library (langdetect)**: Overkill for script detection
- **ML-based detection**: Unnecessary complexity

---

## 6. Agent Tool Chaining

### Decision
Use OpenAI Agents SDK built-in tool chaining with sequential execution.

### Rationale
- Agent can call multiple tools in sequence (list → complete)
- SDK handles tool result passing between calls
- Natural language parsing identifies intent + required tools

### Example Flow
1. User: "Show my tasks and complete the first one"
2. Agent calls `list_tasks(user_id)`
3. Agent receives task list, identifies first task
4. Agent calls `complete_task(user_id, task_id)`
5. Agent returns confirmation message

---

## 7. Error Handling Strategy

### Decision
Graceful error handling with user-friendly messages at all layers.

### Rationale
- Constitution requires no technical stack traces to users
- Each layer catches errors and returns appropriate message
- Logging for debugging, friendly messages for users

### Error Categories
1. **Auth errors (401)**: "Please log in again"
2. **Not found (404)**: "Task not found"
3. **LLM errors**: "I'm having trouble. Please try again."
4. **DB errors**: "Something went wrong. Please try again."

---

## Dependencies Confirmed

| Package | Version | Purpose |
|---------|---------|---------|
| cohere | >=5.0.0 | LLM API client |
| mcp | >=1.0.0 | MCP SDK for tools |
| openai-agents | >=0.1.0 | Agent orchestration |
| @openai/chatkit | >=0.1.0 | Frontend chat UI |

---

## Agents & Skills to Use

| Component | Agent/Skill | Purpose |
|-----------|-------------|---------|
| Chat endpoint | @chatbot-orchestrator | Coordinate request flow |
| Intent parsing | natural-language-parser | Extract user intent |
| MCP tools | @mcp-tool-builder, mcp-tool-craft | Build stateless tools |
| Agent logic | @agent-logic-master | Cohere + tool calling |
| Errors | error-graceful-handler | User-friendly messages |
| DB models | @conversation-persistence-expert | Conversation/Message |
| Frontend | @chatkit-frontend-integrator | ChatKit + icon |
| Responses | confirmation-responder | Friendly confirmations |
