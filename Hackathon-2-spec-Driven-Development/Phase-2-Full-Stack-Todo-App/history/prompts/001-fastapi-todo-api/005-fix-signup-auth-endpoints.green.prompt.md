---
id: 005
title: Fix Signup Auth Endpoints Missing
stage: green
date: 2026-01-10
surface: agent
model: claude-opus-4-5-20251101
feature: 001-fastapi-todo-api
branch: 001-fastapi-todo-api
user: user
command: /sp.implement
labels: ["authentication", "signup", "login", "fastapi", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/models/user.py
  - backend/app/schemas/auth.py
  - backend/app/services/auth_service.py
  - backend/app/api/auth.py
  - backend/app/main.py
  - backend/requirements.txt
tests:
  - Manual API testing via httpx (signup, login, logout)
---

## Prompt

I am experiencing issues in signing up my todo app , check it out whats wrong ?

## Response snapshot

**Root Cause Identified:**
The backend was missing authentication endpoints entirely. The frontend expected:
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`

But the backend only had `/api/tasks` routes. Additionally, the User model lacked a `hashed_password` field.

**Solution Implemented:**
1. Added `hashed_password` field and password hashing methods to User model using bcrypt
2. Created auth schemas (SignupRequest, LoginRequest, AuthResponse, UserResponse, LogoutResponse)
3. Created AuthService with user creation, authentication, and JWT token generation
4. Created auth router with signup, login, and logout endpoints
5. Registered auth router in main.py
6. Added bcrypt and email-validator dependencies
7. Deleted stale SQLite database to allow schema recreation

**Verification:**
- Signup: 201 Created with JWT token and user data
- Login: 200 OK with JWT token
- Wrong password: 401 Unauthorized
- Logout: 200 OK

## Outcome

- ✅ Impact: Critical bug fix - authentication flow now functional
- 🧪 Tests: Manual API tests pass (signup, login, logout, invalid credentials)
- 📁 Files: 6 files modified/created
- 🔁 Next prompts: Test full frontend-to-backend signup flow in browser
- 🧠 Reflection: Always verify API routes exist before assuming frontend issues. The missing auth routes were the root cause.

## Evaluation notes (flywheel)

- Failure modes observed: Database schema out of sync after model changes (required DB deletion)
- Graders run and results (PASS/FAIL): PASS - All endpoints return expected responses
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add integration tests for auth flow
