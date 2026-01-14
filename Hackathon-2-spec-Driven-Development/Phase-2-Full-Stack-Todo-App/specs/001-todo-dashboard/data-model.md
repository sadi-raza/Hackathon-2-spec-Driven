# Data Model: Phase II Todo Dashboard Frontend

**Feature**: 001-todo-dashboard
**Date**: 2025-01-08
**Status**: Complete

## Overview

This document defines the TypeScript interfaces and data structures used by the frontend. These types mirror the backend API responses but are owned by the frontend for type safety.

## Core Entities

### User

```typescript
interface User {
  id: string;
  email: string;
  createdAt: string; // ISO 8601 date string
}

// Session state (stored in auth context)
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

**Validation Rules**:
- `email`: Must be valid email format (validated by Zod)
- `id`: UUID format, read-only from API

### Task

```typescript
interface Task {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: string; // ISO 8601 date string
  updatedAt: string; // ISO 8601 date string
  userId: string;    // Owner reference (not displayed, used for isolation)
}

// For optimistic updates (before server assigns ID)
interface OptimisticTask extends Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'> {
  tempId: string;    // Temporary client-side ID
  isPending: boolean;
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, max 2000 characters
- `completed`: Boolean, default false

## Form Schemas (Zod)

### Login Form

```typescript
const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;
```

### Signup Form

```typescript
const signupSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[a-zA-Z]/, 'Password must contain at least one letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type SignupFormData = z.infer<typeof signupSchema>;
```

### Task Form (Create/Edit)

```typescript
const taskSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less')
    .transform((val) => val.trim()),
  description: z
    .string()
    .max(2000, 'Description must be 2000 characters or less')
    .optional()
    .transform((val) => val?.trim() || null),
});

type TaskFormData = z.infer<typeof taskSchema>;
```

## API Response Types

### Authentication Responses

```typescript
interface AuthResponse {
  user: User;
  token: string; // JWT token (may be in httpOnly cookie instead)
}

interface AuthError {
  error: {
    code: 'INVALID_CREDENTIALS' | 'EMAIL_EXISTS' | 'VALIDATION_ERROR';
    message: string;
  };
}
```

### Task Responses

```typescript
interface TaskListResponse {
  tasks: Task[];
  total: number;
}

interface TaskResponse {
  task: Task;
}

interface TaskError {
  error: {
    code: 'NOT_FOUND' | 'UNAUTHORIZED' | 'VALIDATION_ERROR';
    message: string;
  };
}
```

## UI State Types

### Loading States

```typescript
type LoadingState = 'idle' | 'loading' | 'success' | 'error';

interface AsyncState<T> {
  data: T | null;
  status: LoadingState;
  error: string | null;
}
```

### Modal State

```typescript
interface ModalState {
  isOpen: boolean;
  mode: 'create' | 'edit';
  task: Task | null; // null for create, Task for edit
}
```

### Toast Types

```typescript
type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}
```

## Theme Types

```typescript
type Theme = 'light' | 'dark' | 'system';

interface ThemeState {
  theme: Theme;
  resolvedTheme: 'light' | 'dark'; // Actual applied theme
}
```

## Query Keys (React Query)

```typescript
const queryKeys = {
  tasks: ['tasks'] as const,
  task: (id: string) => ['tasks', id] as const,
  user: ['user'] as const,
} as const;
```

## State Relationships

```
AuthState (global)
├── User (from login/signup)
└── isAuthenticated (derived)

TaskListState (React Query)
├── Task[] (server data)
├── OptimisticTask[] (pending)
└── LoadingState

ModalState (local)
├── isOpen
├── mode (create/edit)
└── selectedTask

ThemeState (next-themes)
├── theme (preference)
└── resolvedTheme (actual)
```

## Data Flow

1. **Authentication Flow**:
   ```
   LoginForm → API → AuthResponse → AuthState → Redirect to Dashboard
   ```

2. **Task CRUD Flow**:
   ```
   TaskForm → Zod Validation → Optimistic Update → API → Reconcile/Rollback
   ```

3. **Theme Flow**:
   ```
   ThemeToggle → next-themes → CSS Variables → UI Update
   ```
