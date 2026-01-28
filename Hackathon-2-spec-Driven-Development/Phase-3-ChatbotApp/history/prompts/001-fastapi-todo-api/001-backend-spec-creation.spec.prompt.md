---
id: 001
title: Backend Spec Creation for FastAPI Todo API
stage: spec
date: 2026-01-09
surface: agent
model: claude-opus-4-5-20251101
feature: 001-fastapi-todo-api
branch: 001-fastapi-todo-api
user: developer
command: /sp.specify
labels: [backend, fastapi, todo-api, jwt-auth, neon-db, specification]
links:
  spec: specs/001-fastapi-todo-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fastapi-todo-api/spec.md
  - specs/001-fastapi-todo-api/checklists/requirements.md
tests:
  - Quality checklist validation: PASSED
---

## Prompt

# Phase II Backend Specification: Secure FastAPI Todo API with Neon DB & JWT Auth

## Objective
Build a secure, production-ready FastAPI backend with Neon PostgreSQL that implements Basic Level CRUD for authenticated users, enforces user isolation via Better Auth JWT, and integrates seamlessly with the Next.js frontend.

## Environment Variables (.env Required)

BETTER_AUTH_SECRET=2026b38e988923a822ac7ba33efa233a87b9ab181d6dae7b4eb62eb2e52e0dbe BETTER_AUTH_URL=http://localhost:3000 DATABASE_URL=postgresql://neondb_owner:npg_vcuQkYmR03di@ep-divine-feather-a7yk4d5h-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

- BETTER_AUTH_SECRET: Shared JWT secret (must match frontend)
- BETTER_AUTH_URL: Frontend base URL for auth callbacks
- DATABASE_URL: Neon connection string

## Core API Endpoints (All Protected by JWT)
1. GET    /api/{user_id}/tasks              # List tasks (query: status, sort)
2. POST   /api/{user_id}/tasks              # Create task
3. GET    /api/{user_id}/tasks/{id}         # Get single task
4. PUT    /api/{user_id}/tasks/{id}         # Update task
5. PATCH  /api/{user_id}/tasks/{id}/complete # Toggle complete
6. DELETE /api/{user_id}/tasks/{id}         # Delete task

## Authentication (Better Auth + JWT)
- JWT token in Authorization: Bearer header
- Verify with BETTER_AUTH_SECRET
- Decode user_id and match path {user_id}
- Invalid/mismatch/expired = 401 Unauthorized
- All endpoints protected

## Database (Neon Serverless Postgres)
- SQLModel ORM
- Models:
  - users: id (str PK), email (unique), name, created_at
  - tasks: id (int PK), user_id (str FK), title (str), description (text), completed (bool), created_at, updated_at
- Indexes: tasks.user_id, tasks.completed
- Auto-create tables on startup
- Always filter by authenticated user_id

## Validation & Security
- Title required (1-200 chars), description optional (max 1000)
- Sanitize inputs
- Ownership: 404 if task not owned
- Consistent responses:
  Success: { "success": true, "data": ..., "message": "..." }
  Error:   { "success": false, "error": "...", "details": [...] }

## Error Handling
- 400: Validation (details)
- 401: Unauthorized
- 404: Not found / not owned
- 500: Internal (generic)

## Frontend Integration
- CORS for http://localhost:3000
- Response format matches frontend
- Ready for optimistic updates

## Tech Stack
- FastAPI
- SQLModel
- Neon PostgreSQL
- PyJWT
- Uvicorn

## Project Structure
backend/
├── main.py           # FastAPI app
├── models.py         # SQLModel models
├── db.py             # Engine + session
├── dependencies.py   # JWT middleware
├── routes/tasks.py   # CRUD routes
├── schemas.py        # Pydantic models
└── utils.py          # Helpers

## Acceptance Criteria
- All endpoints work with JWT auth
- User isolation 100%
- Data persists in Neon DB
- Validation + errors perfect
- Integrates with frontend
- Code 100% Claude generated

## Out of Scope
- Frontend
- Advanced features
- Deployment

This is the complete backend specification for Phase II.

## Response snapshot

Created comprehensive feature specification for FastAPI Todo API Backend:

**Branch**: `001-fastapi-todo-api`
**Spec File**: `specs/001-fastapi-todo-api/spec.md`

### Key Deliverables:

1. **6 User Stories** covering complete CRUD lifecycle:
   - P1: Create Task, View Tasks (foundation)
   - P2: Update Task, Complete/Uncomplete Task (core functionality)
   - P3: Delete Task, View Single Task (lifecycle management)

2. **31 Functional Requirements** organized by category:
   - Authentication & Authorization (FR-001 to FR-004)
   - Task Management (FR-005 to FR-017)
   - Data Isolation (FR-018 to FR-020)
   - Input Handling (FR-021 to FR-023)
   - Response Format (FR-024 to FR-027)
   - Error Handling (FR-028 to FR-031)

3. **Edge Cases** documented for:
   - Validation boundaries (title/description length)
   - Authentication failures (expired, malformed, mismatched)
   - System errors (database unavailable)

4. **Quality Checklist**: All items passed - no clarifications needed

## Outcome

- Impact: Created complete backend API specification ready for implementation planning
- Tests: Quality checklist validation PASSED (all 12 criteria met)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: `/sp.plan` to create implementation plan, `/sp.tasks` to generate tasks
- Reflection: User provided detailed requirements which allowed complete spec without clarifications

## Evaluation notes (flywheel)

- Failure modes observed: None - user requirements were comprehensive
- Graders run and results (PASS/FAIL): Quality checklist PASS
- Prompt variant (if applicable): Standard /sp.specify flow
- Next experiment (smallest change to try): N/A - spec complete
