# API Contract: FastAPI Todo API Backend

**Feature**: `001-fastapi-todo-api`
**Base URL**: `http://localhost:8000/api`
**Authentication**: Bearer Token (JWT)
**Date**: 2026-01-09

---

## Authentication

All endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

**Token Source**: Better Auth (frontend)
**User Extraction**: `sub` claim from JWT payload

---

## Response Format

### Success Response

```json
{
  "task": { ... }
}
// or for lists:
{
  "tasks": [ ... ],
  "total": 5
}
```

### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description"
  }
}
```

**Error Codes**:
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing/invalid/expired token |
| `NOT_FOUND` | 404 | Task not found or not owned |
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Endpoints

### 1. List Tasks

**GET** `/api/tasks`

Retrieve all tasks for the authenticated user.

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | `all` | Filter: `completed`, `incomplete`, `all` |
| `sort` | string | No | `created_at` | Sort by: `created_at`, `title` |

**Request**:
```http
GET /api/tasks?status=incomplete&sort=created_at HTTP/1.1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T10:00:00Z",
      "userId": "user-123"
    }
  ],
  "total": 1
}
```

**Errors**:
- 401: Invalid or missing token

---

### 2. Create Task

**POST** `/api/tasks`

Create a new task for the authenticated user.

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 1-200 characters |
| `description` | string | No | Max 1000 characters |

**Request**:
```http
POST /api/tasks HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "createdAt": "2026-01-09T10:00:00Z",
    "updatedAt": "2026-01-09T10:00:00Z",
    "userId": "user-123"
  }
}
```

**Errors**:
- 400: Validation error (title too long, empty, etc.)
- 401: Invalid or missing token

---

### 3. Get Single Task

**GET** `/api/tasks/{id}`

Retrieve a specific task by ID.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Task UUID |

**Request**:
```http
GET /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "createdAt": "2026-01-09T10:00:00Z",
    "updatedAt": "2026-01-09T10:00:00Z",
    "userId": "user-123"
  }
}
```

**Errors**:
- 401: Invalid or missing token
- 404: Task not found OR not owned by user

---

### 4. Update Task

**PUT** `/api/tasks/{id}`

Update a task's title and/or description.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Task UUID |

**Request Body**:
```json
{
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | No | 1-200 characters if provided |
| `description` | string | No | Max 1000 characters |
| `completed` | boolean | No | true/false |

**Request**:
```http
PUT /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy organic groceries"
}
```

**Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy organic groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "createdAt": "2026-01-09T10:00:00Z",
    "updatedAt": "2026-01-09T11:00:00Z",
    "userId": "user-123"
  }
}
```

**Errors**:
- 400: Validation error
- 401: Invalid or missing token
- 404: Task not found OR not owned by user

---

### 5. Toggle Task Completion

**PATCH** `/api/tasks/{id}`

Toggle the completion status of a task.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Task UUID |

**Request Body**:
```json
{
  "completed": true
}
```

**Request**:
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "createdAt": "2026-01-09T10:00:00Z",
    "updatedAt": "2026-01-09T12:00:00Z",
    "userId": "user-123"
  }
}
```

**Errors**:
- 401: Invalid or missing token
- 404: Task not found OR not owned by user

---

### 6. Delete Task

**DELETE** `/api/tasks/{id}`

Permanently delete a task.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Task UUID |

**Request**:
```http
DELETE /api/tasks/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Errors**:
- 401: Invalid or missing token
- 404: Task not found OR not owned by user

---

## Data Types

### Task Object

```typescript
interface Task {
  id: string;           // UUID
  title: string;        // 1-200 chars
  description: string | null;  // Max 1000 chars
  completed: boolean;   // Default: false
  createdAt: string;    // ISO 8601 UTC
  updatedAt: string;    // ISO 8601 UTC
  userId: string;       // User ID from JWT
}
```

### Error Object

```typescript
interface ApiError {
  error: {
    code: string;       // Error code
    message: string;    // Human-readable
  }
}
```

---

## Security Notes

1. **User Isolation**: All task queries filtered by authenticated user's ID
2. **404 for Authorization**: Return 404 (not 403) when user doesn't own task
3. **Token Validation**: Verify signature, expiration, and `sub` claim
4. **Input Sanitization**: Trim whitespace, validate lengths

---

## Frontend Integration

The frontend (`frontend/lib/api.ts`) expects these exact endpoints and response formats:

```typescript
// Frontend API client methods
api.tasks.list()              // GET /api/tasks
api.tasks.create(data)        // POST /api/tasks
api.tasks.update(id, data)    // PUT /api/tasks/:id
api.tasks.delete(id)          // DELETE /api/tasks/:id
```

**CORS Origin**: `http://localhost:3000`

---

## References

- Spec: `specs/001-fastapi-todo-api/spec.md`
- Frontend API: `frontend/lib/api.ts`
- Frontend Types: `frontend/types/index.ts`
