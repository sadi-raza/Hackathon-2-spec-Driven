---
id: 007
title: Stale Server Cache Fix for Chatbot Errors
stage: green
date: 2025-01-27
surface: agent
model: claude-opus-4-5-20251101
feature: 002-ai-todo-chatbot
branch: 002-ai-todo-chatbot
user: developer
command: /sp.implement
labels: ["debugging", "server", "pydantic", "validation", "cache"]
links:
  spec: specs/002-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/schemas/chat.py (already fixed in 006)
tests:
  - Add task via chat: PASS
  - List tasks via chat: PASS
---

## Prompt

this error in chatbot during chatting 500 Internal Server Error aur pydantic validation errors

## Response snapshot

### Root Cause Analysis

The 500 Internal Server Error with Pydantic validation errors was caused by **stale server instances** running with old cached code:

```
ERROR:root:Chat processing error: 2 validation errors for ToolCallResult
arguments
  Field required [type=missing, input_value={'tool': 'add_task', 'suc...es' added successfully"}, input_type=dict]
result
  Input should be a valid dictionary [type=dict_type, input_value="Task 'buy groceries' added successfully", input_type=str]
```

### Issue Explanation

The schema fix from PHR 006 had been applied to `backend/app/schemas/chat.py`, but **multiple old server instances** were still running on ports 8000 and 8001 with the cached old schema that expected:
- `arguments: dict` (required field)
- `result: dict`

While the new schema correctly uses:
- `success: bool`
- `result: Optional[str]`

### Resolution

1. Killed all stale server instances
2. Started fresh server on port 8000 with latest code
3. Verified chatbot API returns 200 OK with correct response format

### Test Results

```json
// Add task - SUCCESS
{"conversation_id":"3ef0247a-8b69-4d70-9c92-baffbe782b41","response":"Task 'buy milk' added successfully","tool_calls":[{"tool":"add_task","success":true,"result":"Task 'buy milk' added successfully"}]}

// List tasks - SUCCESS
{"conversation_id":"00ead08f-7587-4627-b89b-659796ca12b7","response":"Found 1 task(s)","tool_calls":[{"tool":"list_tasks","success":true,"result":"Found 1 task(s)"}]}
```

## Outcome

- Impact: Resolved 500 errors by restarting server to clear cached code
- Tests: 2/2 tests passed (add_task, list_tasks via chat)
- Files: No code changes needed - fix was already in place from PHR 006
- Next prompts: Test Urdu language support, test frontend integration
- Reflection: Always restart server after code changes to avoid stale cache issues

## Evaluation notes (flywheel)

- Failure modes observed: Stale server cache running old code after schema changes
- Graders run and results (PASS/FAIL): PASS - All API calls returning 200 OK
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add uvicorn --reload flag for development to auto-reload on code changes
