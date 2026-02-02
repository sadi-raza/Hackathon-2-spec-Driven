# Research: FastAPI Todo API Backend

**Feature**: `001-fastapi-todo-api`
**Date**: 2026-01-09
**Status**: Complete

## Executive Summary

This document consolidates research findings for implementing the Phase II backend: a secure FastAPI Todo API with Neon PostgreSQL and Better Auth JWT integration. All technical unknowns have been resolved.

---

## 1. JWT Authentication with Better Auth

### Decision: Use `sub` claim for user identification

**Rationale**: The JWT standard (RFC 7519) specifies `sub` (subject) as the primary user identifier. Better Auth follows OAuth2/OIDC conventions and places user ID in the `sub` claim.

**Token Structure** (expected from Better Auth):
```json
{
  "sub": "user-id-string",
  "email": "user@example.com",
  "iat": 1704067200,
  "exp": 1704153600
}
```

**Alternatives Considered**:
- `userId` claim: Non-standard, app-specific
- Path-based user_id: Frontend uses `/tasks` not `/api/{user_id}/tasks`

### Decision: Simplify API paths (no user_id in URL)

**Rationale**: The existing frontend (`frontend/lib/api.ts`) uses:
- `GET /tasks` (not `/api/{user_id}/tasks`)
- `POST /tasks`
- `PUT /tasks/:id`
- `DELETE /tasks/:id`

The backend extracts user_id from the JWT token, not the URL path. This is cleaner and prevents URL manipulation attacks.

### Implementation Pattern

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## 2. Database: SQLModel with Neon PostgreSQL

### Decision: Use async SQLModel with connection pooling

**Rationale**: Neon is serverless; connections may be suspended. Async sessions with proper pooling ensure reliability.

**Connection Configuration**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Neon-optimized settings
engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=3,           # Small for serverless
    max_overflow=2,
    pool_timeout=10,
    pool_recycle=3600,     # Recycle every hour
    pool_pre_ping=True,    # Verify connection alive
)
```

### Decision: Use string IDs for tasks (not integers)

**Rationale**: Frontend types (`frontend/types/index.ts`) define `Task.id` as `string`. Use UUID strings for consistency with frontend expectations.

**Alternatives Considered**:
- Auto-increment integers: Spec suggested this, but frontend expects strings
- Resolution: Use UUIDs (generated as strings) for better frontend compatibility

### Model Definitions

```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(primary_key=True)  # Better Auth user ID
    email: str = Field(unique=True, index=True)
    name: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_user_completed", "user_id", "completed"),
    )
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 3. API Response Format

### Decision: Match frontend expected format

**Rationale**: Frontend (`frontend/types/index.ts`) expects specific response structures.

**Task List Response**:
```json
{
  "tasks": [...],
  "total": 5
}
```

**Single Task Response**:
```json
{
  "task": {...}
}
```

**Error Response** (from `ApiError` type):
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

### Decision: Return 404 for ownership violations

**Rationale**: Spec requirement FR-019 - return 404 (not 403) to prevent user enumeration attacks.

---

## 4. Input Validation & Sanitization

### Decision: Use Pydantic field validators

**Implementation**:
```python
from pydantic import field_validator

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator('title', 'description')
    @classmethod
    def trim_whitespace(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Cannot be empty or whitespace only')
        return v
```

---

## 5. CORS Configuration

### Decision: Allow only frontend origin

**Rationale**: Single frontend application at `http://localhost:3000`.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 6. Project Structure

### Decision: Standard FastAPI modular structure

```
backend/
├── main.py              # FastAPI app, lifespan, CORS
├── config.py            # Settings from environment
├── database.py          # Engine, session, create_tables
├── models.py            # SQLModel entities (User, Task)
├── schemas.py           # Pydantic request/response models
├── dependencies.py      # JWT auth dependency
├── routes/
│   └── tasks.py         # Task CRUD endpoints
└── requirements.txt     # Python dependencies
```

---

## 7. Technology Stack (Confirmed)

| Component | Choice | Version |
|-----------|--------|---------|
| Framework | FastAPI | 0.109+ |
| ORM | SQLModel | 0.0.14+ |
| Database | Neon PostgreSQL | Serverless |
| Async Driver | asyncpg | 0.29+ |
| JWT | PyJWT | 2.8+ |
| Server | Uvicorn | 0.27+ |
| Validation | Pydantic | 2.5+ |

---

## 8. Resolved Clarifications

| Item | Resolution |
|------|------------|
| JWT claim for user ID | Use `sub` claim (standard) |
| API path structure | `/api/tasks` (no user_id in path) |
| Task ID type | String (UUID) to match frontend |
| Session management | Async with SQLModel |
| Connection pooling | Small pool (3+2) for Neon serverless |
| Error response format | Match frontend `ApiError` type |

---

## References

- Frontend API client: `frontend/lib/api.ts`
- Frontend types: `frontend/types/index.ts`
- Feature spec: `specs/001-fastapi-todo-api/spec.md`
- Constitution: `.specify/memory/constitution.md`
