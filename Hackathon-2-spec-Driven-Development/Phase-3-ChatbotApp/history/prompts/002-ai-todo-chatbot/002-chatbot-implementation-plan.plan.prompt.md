---
id: 002
title: Chatbot Implementation Plan
stage: plan
date: 2025-01-16
surface: agent
model: claude-opus-4-5-20251101
feature: 002-ai-todo-chatbot
branch: 002-ai-todo-chatbot
user: architect
command: /sp.plan
labels: ["phase-iii", "chatbot", "plan", "architecture", "mcp", "cohere"]
links:
  spec: specs/002-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-ai-todo-chatbot/plan.md
  - specs/002-ai-todo-chatbot/research.md
  - specs/002-ai-todo-chatbot/data-model.md
  - specs/002-ai-todo-chatbot/quickstart.md
  - specs/002-ai-todo-chatbot/contracts/chat-api.yaml
  - specs/002-ai-todo-chatbot/contracts/mcp-tools.md
tests:
  - N/A (planning phase)
---

## Prompt

Read speckit.constitution and the complete speckit.specify-chatbot specification carefully.

You are building Phase III: AI Todo Chatbot directly integrated into the existing Phase II full-stack app (Next.js frontend + FastAPI backend with Neon DB & JWT).

Key rules:
- Extend existing FastAPI backend (no new server)
- Use Cohere API key for ALL LLM reasoning (OpenAI Agents SDK compatible)
- Reuse Phase II JWT middleware, SQLModel, DB connection
- Add floating chatbot icon on frontend dashboard
- Stateless design: conversation state in Neon DB only

Use these agents and skills:
- @chatbot-orchestrator with natural-language-parser and confirmation-responder
- @mcp-tool-builder with mcp-tool-craft
- @agent-logic-master with error-graceful-handler
- @conversation-persistence-expert with conversation-state-manager
- @chatkit-frontend-integrator with api-client-builder

Generate a concise, actionable speckit.plan-chatbot with this structure:

1. High-Level Architecture
2. Database Extensions
3. MCP Server Implementation
4. Chat Endpoint (/api/{user_id}/chat)
5. Agent Logic (OpenAI Agents SDK)
6. Frontend Integration (ChatKit + Icon)
7. Bonus: Urdu Detection
8. Testing & Verification

## Response snapshot

Generated complete Phase III implementation plan with all artifacts:

**Artifacts Created:**
1. `research.md` - Technical research with 7 decisions:
   - Cohere API integration pattern
   - MCP SDK integration strategy
   - Conversation persistence design
   - ChatKit frontend integration
   - Urdu language detection
   - Agent tool chaining
   - Error handling strategy

2. `data-model.md` - Database schema:
   - Conversation table (id, user_id, title, timestamps)
   - Message table (id, conversation_id, user_id, role, content, tool_calls, created_at)
   - Relationships and indexes

3. `contracts/chat-api.yaml` - OpenAPI spec:
   - POST /{user_id}/chat
   - GET /{user_id}/conversations
   - GET /{user_id}/conversations/{id}

4. `contracts/mcp-tools.md` - 5 MCP tool signatures:
   - add_task, list_tasks, complete_task, delete_task, update_task

5. `quickstart.md` - Setup and verification guide

6. `plan.md` - Complete implementation plan with:
   - Technical context (all checks PASS)
   - Constitution check (10/10 principles verified)
   - Project structure (backend + frontend directories)
   - 8 sections matching user request structure
   - Agent/skill mapping for implementation

**Constitution Check Results:** All 10 principles PASSED

## Outcome

- ✅ Impact: Complete implementation plan ready for /sp.tasks
- 🧪 Tests: N/A (planning phase - no code yet)
- 📁 Files: 6 artifacts created
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Comprehensive plan covers all 8 requested sections with clear agent/skill delegation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution check 10/10
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
