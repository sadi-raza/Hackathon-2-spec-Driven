# API Contract: Phase II Todo Dashboard Frontend

**Feature**: 001-todo-dashboard
**Date**: 2025-01-08
**Version**: 1.0.0

## Overview

This document defines the API contracts the frontend expects from the backend. The frontend is designed to work with these endpoints and response formats.

## Base URL

```
API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
```

## Authentication Endpoints

### POST /auth/signup

Create a new user account.

**Request**:
```typescript
{
  email: string;    // Valid email format
  password: string; // Minimum 8 characters
}
```

**Response 201**:
```typescript
{
  user: {
    id: string;
    email: string;
    createdAt: string;
  };
  token: string; // JWT token (or set via httpOnly cookie)
}
```

**Response 400** (Validation Error):
```typescript
{
  error: {
    code: "VALIDATION_ERROR";
    message: "Invalid email format" | "Password too short";
  }
}
```

**Response 409** (Conflict):
```typescript
{
  error: {
    code: "EMAIL_EXISTS";
    message: "An account with this email already exists";
  }
}
```

---

### POST /auth/login

Authenticate existing user.

**Request**:
```typescript
{
  email: string;
  password: string;
}
```

**Response 200**:
```typescript
{
  user: {
    id: string;
    email: string;
    createdAt: string;
  };
  token: string;
}
```

**Response 401** (Unauthorized):
```typescript
{
  error: {
    code: "INVALID_CREDENTIALS";
    message: "Invalid email or password";
  }
}
```

---

### POST /auth/logout

End user session.

**Headers**:
```
Authorization: Bearer <token>
```

**Response 200**:
```typescript
{
  message: "Logged out successfully"
}
```

---

## Task Endpoints

All task endpoints require authentication.

**Headers** (required for all):
```
Authorization: Bearer <token>
Content-Type: application/json
```

### GET /tasks

Fetch all tasks for authenticated user.

**Response 200**:
```typescript
{
  tasks: Array<{
    id: string;
    title: string;
    description: string | null;
    completed: boolean;
    createdAt: string;
    updatedAt: string;
    userId: string;
  }>;
  total: number;
}
```

**Response 401**:
```typescript
{
  error: {
    code: "UNAUTHORIZED";
    message: "Authentication required";
  }
}
```

---

### POST /tasks

Create a new task.

**Request**:
```typescript
{
  title: string;              // Required, 1-200 chars
  description?: string | null; // Optional, max 2000 chars
}
```

**Response 201**:
```typescript
{
  task: {
    id: string;
    title: string;
    description: string | null;
    completed: false;
    createdAt: string;
    updatedAt: string;
    userId: string;
  }
}
```

**Response 400** (Validation Error):
```typescript
{
  error: {
    code: "VALIDATION_ERROR";
    message: "Title is required" | "Title too long";
  }
}
```

---

### PUT /tasks/:id

Update an existing task.

**URL Parameters**:
- `id`: Task UUID

**Request**:
```typescript
{
  title?: string;              // Optional, 1-200 chars
  description?: string | null; // Optional, max 2000 chars
  completed?: boolean;         // Optional
}
```

**Response 200**:
```typescript
{
  task: {
    id: string;
    title: string;
    description: string | null;
    completed: boolean;
    createdAt: string;
    updatedAt: string;
    userId: string;
  }
}
```

**Response 404**:
```typescript
{
  error: {
    code: "NOT_FOUND";
    message: "Task not found";
  }
}
```

**Response 403** (Forbidden - wrong user):
```typescript
{
  error: {
    code: "FORBIDDEN";
    message: "You do not have permission to modify this task";
  }
}
```

---

### DELETE /tasks/:id

Delete a task.

**URL Parameters**:
- `id`: Task UUID

**Response 200**:
```typescript
{
  message: "Task deleted successfully"
}
```

**Response 404**:
```typescript
{
  error: {
    code: "NOT_FOUND";
    message: "Task not found";
  }
}
```

---

## Error Response Format

All error responses follow this structure:

```typescript
interface ErrorResponse {
  error: {
    code: string;    // Machine-readable error code
    message: string; // Human-readable message (safe to display)
    details?: Record<string, string>; // Optional field-level errors
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | User doesn't own resource |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `EMAIL_EXISTS` | 409 | Email already registered |
| `INVALID_CREDENTIALS` | 401 | Wrong email/password |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Frontend API Client Implementation

```typescript
// lib/api.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Handle session expiry
      window.location.href = '/login?session=expired';
      throw new Error('Session expired');
    }

    const data = await response.json();

    if (!response.ok) {
      throw new ApiError(data.error.code, data.error.message);
    }

    return data;
  }

  // Auth methods
  auth = {
    signup: (email: string, password: string) =>
      this.request<AuthResponse>('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),

    login: (email: string, password: string) =>
      this.request<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),

    logout: () =>
      this.request<{ message: string }>('/auth/logout', {
        method: 'POST',
      }),
  };

  // Task methods
  tasks = {
    list: () => this.request<TaskListResponse>('/tasks'),

    create: (data: { title: string; description?: string }) =>
      this.request<TaskResponse>('/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    update: (id: string, data: Partial<Task>) =>
      this.request<TaskResponse>(`/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),

    delete: (id: string) =>
      this.request<{ message: string }>(`/tasks/${id}`, {
        method: 'DELETE',
      }),
  };
}

export const api = new ApiClient();
```

---

## CORS Requirements

The backend must allow:

```
Access-Control-Allow-Origin: http://localhost:3000 (dev) | https://your-domain.com (prod)
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true (if using cookies)
```
