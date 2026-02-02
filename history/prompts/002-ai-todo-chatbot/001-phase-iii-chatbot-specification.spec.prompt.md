---
id: 001
title: Phase III Chatbot Specification
stage: spec
date: 2025-01-16
surface: agent
model: claude-opus-4-5-20251101
feature: 002-ai-todo-chatbot
branch: 002-ai-todo-chatbot
user: architect
command: /sp.specify
labels: ["phase-iii", "chatbot", "ai", "mcp", "cohere", "specification"]
links:
  spec: specs/002-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-ai-todo-chatbot/spec.md
  - specs/002-ai-todo-chatbot/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

# Phase III Specification: AI-Powered Todo Chatbot Integration

## Objective

Extend the Phase II full-stack application (Next.js frontend + FastAPI backend with Neon DB & Better Auth JWT) to add a conversational AI chatbot that manages Todo tasks via natural language. The chatbot uses OpenAI ChatKit UI (frontend), Cohere API key for LLM reasoning, OpenAI Agents SDK for agent logic, and Official MCP SDK for stateless task tools. All development is 100% spec-driven with Claude Code.

## Core Requirements

1. Stateless Chat Endpoint
   - POST /api/{user_id}/chat (extends Phase II backend)
   - Input: { "message": string, "conversation_id": int (optional) }
   - Output: { "conversation_id": int, "response": string, "tool_calls": array }
   - Requires valid JWT from Phase II

2. MCP Server (Official MCP SDK)
   - Run inside existing FastAPI backend
   - Expose 5 stateless tools (all filter by user_id from JWT):
     - add_task, list_tasks, complete_task, delete_task, update_task
   - Reuse Phase II SQLModel Task model and DB session

3. AI Agent Logic (OpenAI Agents SDK)
   - Use Cohere API key for all LLM reasoning
   - Agent parses natural language (English + Urdu detection)
   - Chains tools when needed
   - Handles errors gracefully

4. Conversation Persistence (Stateless Design)
   - New SQLModel models: Conversation, Message
   - Server holds NO state – fetch history from DB on each request

5. Frontend Integration (OpenAI ChatKit + Icon)
   - Add floating chatbot icon on dashboard
   - ChatKit sends messages to /api/{user_id}/chat with JWT

6. Bonus: Urdu Support (+100)
   - Detect Urdu script in user message
   - Respond in Urdu when detected

## Response snapshot

Created comprehensive Phase III specification with:

**Branch**: `002-ai-todo-chatbot`
**Spec File**: `specs/002-ai-todo-chatbot/spec.md`

**User Stories (7 total)**:
- US1: Add Task via Chat (P1)
- US2: List Tasks via Chat (P1)
- US3: Complete Task via Chat (P2)
- US4: Delete Task via Chat (P2)
- US5: Update Task via Chat (P3)
- US6: Conversation History Persistence (P2)
- US7: Chatbot Icon and Interface (P1)

**Functional Requirements**: FR-001 through FR-014 covering:
- Stateless chat endpoint with JWT auth
- 5 MCP tools with user isolation
- Conversation/Message persistence in Neon DB
- Cohere API for LLM reasoning
- ChatKit frontend integration
- Urdu language support

**Checklist Validation**: 16/16 items PASSED
- All requirements testable and unambiguous
- No [NEEDS CLARIFICATION] markers
- Success criteria measurable and technology-agnostic

## Outcome

- ✅ Impact: Complete Phase III specification ready for planning
- 🧪 Tests: N/A (specification phase - no code yet)
- 📁 Files: 2 created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Comprehensive user input enabled full spec without clarification questions

## Evaluation notes (flywheel)

- Failure modes observed: None - user input was comprehensive
- Graders run and results (PASS/FAIL): PASS - checklist 16/16
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
