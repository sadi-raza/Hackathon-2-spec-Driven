# FastAPI Todo API Backend

Secure task management API for authenticated users built with FastAPI, SQLModel, and Neon PostgreSQL.

## Overview

This backend provides a complete task management system that:
- Validates JWT tokens from Better Auth
- Enforces complete user isolation
- Returns consistent JSON responses
- Integrates with existing Next.js frontend

## Features

- **User Authentication**: JWT token validation
- **Task Management**: Create, read, update, delete tasks
- **User Isolation**: Users can only access their own tasks
- **Filtering**: Filter tasks by completion status
- **Validation**: Input validation and sanitization

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLModel with Neon PostgreSQL
- **Authentication**: JWT with PyJWT
- **Testing**: pytest, httpx
- **Async Driver**: asyncpg

## API Endpoints

### Tasks
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete a task

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

Run tests with pytest:
```bash
pytest
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT validation
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `DEBUG`: Enable debug mode (default: false)

## Architecture

The application follows a clean architecture pattern:
- **API Layer**: FastAPI routes and dependency injection
- **Service Layer**: Business logic in TaskService
- **Data Layer**: SQLModel models and database operations
- **Middleware**: JWT authentication and CORS

---

## Phase III: AI Chatbot Integration

Phase III adds an AI-powered chatbot that allows users to manage tasks via natural language.

### Additional Features

- **Chat Interface**: Natural language task management
- **MCP Tools**: Stateless tool operations (add, list, complete, delete, update)
- **Conversation Persistence**: Chat history stored in database
- **Urdu Support**: Detects Urdu and responds appropriately (+100 bonus)
- **Cohere LLM**: All AI reasoning uses Cohere API

### New API Endpoints

#### Chat
- `POST /api/{user_id}/chat` - Send a chat message
  - Request: `{ "message": "Add buy milk", "conversation_id": "optional" }`
  - Response: `{ "conversation_id": "...", "response": "...", "tool_calls": [...] }`

#### Conversations
- `GET /api/{user_id}/conversations` - List user's conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation with messages

### Additional Environment Variables

```bash
COHERE_API_KEY=your-cohere-api-key  # Required for Phase III
```

### New Dependencies

```bash
pip install cohere mcp openai-agents
```

### Chat Flow

1. User sends message to `/api/{user_id}/chat`
2. ChatService creates/gets conversation
3. TodoAgent processes message with Cohere LLM
4. MCP tools execute task operations
5. Response and tool calls saved to database
6. Response returned to frontend

### Urdu Support

Messages containing Urdu/Arabic script (U+0600-U+06FF) are detected and:
- Agent uses Urdu system prompt
- Confirmations returned in Urdu
- Example: "کام 'دودھ خریدنا' شامل کر دیا گیا!"

### Testing the Chatbot

```bash
# Get JWT token first, then:
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries"}'
```