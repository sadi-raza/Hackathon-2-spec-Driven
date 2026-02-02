# Data Model: FastAPI Todo API Backend

**Feature**: `001-fastapi-todo-api`
**Date**: 2026-01-09
**Database**: Neon PostgreSQL (Serverless)

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         users                                │
├─────────────────────────────────────────────────────────────┤
│ id          │ VARCHAR(255) │ PK          │ Better Auth ID   │
│ email       │ VARCHAR(255) │ UNIQUE, IDX │                  │
│ name        │ VARCHAR(255) │ NULLABLE    │                  │
│ created_at  │ TIMESTAMP    │ NOT NULL    │ UTC              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         tasks                                │
├─────────────────────────────────────────────────────────────┤
│ id          │ VARCHAR(36)  │ PK          │ UUID string      │
│ user_id     │ VARCHAR(255) │ FK, IDX     │ → users.id       │
│ title       │ VARCHAR(200) │ NOT NULL    │                  │
│ description │ TEXT         │ NULLABLE    │ Max 1000 chars   │
│ completed   │ BOOLEAN      │ NOT NULL    │ Default: false   │
│ created_at  │ TIMESTAMP    │ NOT NULL    │ UTC              │
│ updated_at  │ TIMESTAMP    │ NOT NULL    │ UTC              │
└─────────────────────────────────────────────────────────────┘
```

## Entity: User

**Purpose**: Represents an authenticated user from Better Auth.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | VARCHAR(255) | PK | User ID from Better Auth (string) |
| `email` | VARCHAR(255) | UNIQUE, INDEX | User's email address |
| `name` | VARCHAR(255) | NULLABLE | User's display name |
| `created_at` | TIMESTAMP | NOT NULL | Account creation time (UTC) |

**Notes**:
- Users are created by Better Auth; backend may create on first task if needed
- The `id` field matches Better Auth's user identifier

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Entity: Task

**Purpose**: Represents a todo item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | VARCHAR(36) | PK | UUID string (auto-generated) |
| `user_id` | VARCHAR(255) | FK → users.id, INDEX | Owner's user ID |
| `title` | VARCHAR(200) | NOT NULL | Task title (1-200 chars) |
| `description` | TEXT | NULLABLE | Optional details (max 1000 chars) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL | Creation time (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL | Last modification time (UTC) |

**Indexes**:
- `idx_tasks_user_id`: On `user_id` for user isolation queries
- `idx_tasks_completed`: On `completed` for status filtering
- `idx_user_completed`: Composite on `(user_id, completed)` for filtered queries

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Index
from datetime import datetime
from uuid import uuid4

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_user_completed", "user_id", "completed"),
    )

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        max_length=36
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=255
    )
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Validation Rules

### Task Title
- **Required**: Yes
- **Min Length**: 1 character (after trimming whitespace)
- **Max Length**: 200 characters
- **Sanitization**: Trim leading/trailing whitespace

### Task Description
- **Required**: No
- **Max Length**: 1000 characters
- **Sanitization**: Trim leading/trailing whitespace

### Pydantic Schemas

```python
from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator('title', 'description', mode='before')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v):
        if not v:
            raise ValueError('Title cannot be empty')
        return v

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
```

---

## State Transitions

### Task Lifecycle

```
                    ┌──────────────┐
      POST /tasks   │              │
    ───────────────►│   Created    │
                    │ completed=F  │
                    └──────┬───────┘
                           │
                           │ PATCH /tasks/{id}/complete
                           ▼
                    ┌──────────────┐
                    │              │
                    │  Completed   │◄────┐
                    │ completed=T  │     │ Toggle
                    └──────┬───────┘─────┘
                           │
                           │ DELETE /tasks/{id}
                           ▼
                    ┌──────────────┐
                    │              │
                    │   Deleted    │
                    │  (removed)   │
                    └──────────────┘
```

**Valid Transitions**:
1. Create → Task exists with `completed=false`
2. Complete → Toggle `completed` between true/false
3. Update → Modify `title` or `description`, updates `updated_at`
4. Delete → Permanent removal (hard delete)

---

## Data Integrity Constraints

| Constraint | Type | Enforcement |
|------------|------|-------------|
| User owns task | FK + Query | `user_id` FK + WHERE clause |
| Title required | NOT NULL | Database + Pydantic |
| Title length | CHECK | Pydantic (max_length=200) |
| Description length | CHECK | Pydantic (max_length=1000) |
| Timestamps UTC | DEFAULT | `datetime.utcnow` |

---

## Query Patterns

### List User's Tasks (with filters)
```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND (:status IS NULL OR completed = :completed)
ORDER BY created_at DESC;
```

### Get Single Task (with ownership check)
```sql
SELECT * FROM tasks
WHERE id = :task_id AND user_id = :user_id;
```

### Create Task
```sql
INSERT INTO tasks (id, user_id, title, description, completed, created_at, updated_at)
VALUES (:id, :user_id, :title, :description, false, NOW(), NOW())
RETURNING *;
```

### Update Task
```sql
UPDATE tasks
SET title = COALESCE(:title, title),
    description = COALESCE(:description, description),
    completed = COALESCE(:completed, completed),
    updated_at = NOW()
WHERE id = :task_id AND user_id = :user_id
RETURNING *;
```

### Delete Task
```sql
DELETE FROM tasks
WHERE id = :task_id AND user_id = :user_id;
```

---

## Migration Strategy

### Initial Schema (create_all)

For Phase II, use SQLModel's `create_all()` on startup:

```python
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Future Migrations (Alembic)

When schema changes are needed:
```bash
alembic init alembic
alembic revision --autogenerate -m "add_priority_field"
alembic upgrade head
```

---

## References

- Spec: `specs/001-fastapi-todo-api/spec.md` (FR-005 to FR-017)
- Research: `specs/001-fastapi-todo-api/research.md`
- Frontend Types: `frontend/types/index.ts`
