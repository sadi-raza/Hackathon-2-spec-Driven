# Quickstart: AI-Powered Todo Chatbot

**Feature**: 002-ai-todo-chatbot
**Date**: 2025-01-16

## Prerequisites

- Phase II backend and frontend running
- Node.js 18+ and Python 3.11+
- Neon DB connection (existing from Phase II)
- Cohere API key

---

## 1. Environment Setup

Add to your `.env` file:

```bash
# Existing Phase II variables
BETTER_AUTH_SECRET=your-auth-secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...

# NEW Phase III variables
COHERE_API_KEY=your-cohere-api-key
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-chatkit-domain-key
```

---

## 2. Backend Dependencies

```bash
cd backend
pip install cohere mcp openai-agents
```

---

## 3. Frontend Dependencies

```bash
cd frontend
npm install @openai/chatkit
```

---

## 4. Verify Chatbot

### Test via curl

```bash
# Login first to get JWT token
TOKEN="your-jwt-token"
USER_ID="your-user-id"

# Send a chat message
curl -X POST "http://localhost:8000/api/${USER_ID}/chat" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries to my list"}'
```

Expected response:
```json
{
  "conversation_id": "abc-123",
  "response": "Task 'buy groceries' added!",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {"title": "buy groceries"},
      "result": {"task_id": "xyz", "status": "created"}
    }
  ]
}
```

### Test via UI

1. Open http://localhost:3000/dashboard
2. Click the floating chat icon (bottom-right)
3. Type "Show my tasks"
4. Verify tasks are listed

---

## 5. Test Urdu Support

```bash
# Urdu message test
curl -X POST "http://localhost:8000/api/${USER_ID}/chat" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "میری لسٹ میں دودھ خریدنا شامل کریں"}'
```

Expected: Response in Urdu confirming task creation.

---

## 6. Verification Checklist

- [ ] Backend starts without errors
- [ ] Chat endpoint responds to messages
- [ ] Tasks created via chat appear in dashboard
- [ ] Conversation persists on page refresh
- [ ] Chat icon visible on dashboard
- [ ] ChatKit UI opens on icon click
- [ ] Urdu messages get Urdu responses

---

## Troubleshooting

### "Cohere API error"
- Check COHERE_API_KEY is set correctly
- Verify API key has quota remaining

### "Conversation not loading"
- Check database connection
- Verify Conversation/Message tables created

### "Chat icon not visible"
- Check frontend built and deployed
- Verify ChatKit package installed

### "401 Unauthorized"
- JWT token expired - re-login
- Check Authorization header format: `Bearer <token>`
