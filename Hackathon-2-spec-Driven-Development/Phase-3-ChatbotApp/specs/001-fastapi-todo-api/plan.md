# Implementation Plan: FastAPI Todo API Backend

**Branch**: `001-fastapi-todo-api` | **Date**: 2026-01-09 | **Spec**: `/specs/001-fastapi-todo-api/spec.md`
**Input**: Phase II Backend - Secure FastAPI Todo API with Neon DB & JWT Auth

## Summary

Build a production-ready FastAPI backend that provides secure task management for authenticated users. The API uses SQLModel with Neon PostgreSQL, validates JWT tokens from Better Auth, enforces complete user isolation, and returns consistent JSON responses matching the existing Next.js frontend contracts.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, python-dotenv, uvicorn, asyncpg
**Storage**: Neon PostgreSQL (serverless Postgres)
**Testing**: pytest, pytest-asyncio, httpx (async test client)
**Target Platform**: Linux/Windows server (development), Neon cloud (production DB)
**Project Type**: Web API (backend only - frontend exists)
**Performance Goals**: <500ms p95 latency, 100 concurrent users
**Constraints**: JWT validation only (no token issuance), user isolation at query level
**Scale/Scope**: Single-tenant API, ~1000 tasks per user max

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| I. Zero Manual Coding | PASS | All code generated via Claude Code with spec references |
| II. Spec-Driven Development | PASS | Plan traces: Task ID → Plan → Spec → Constitution |
| III. Reusable Intelligence | PASS | Using agents: @crud-perfectionist, @database-genius, @security-fortress-master, @integration-tester |
| IV. Phase Evolution | PASS | Phase II implementation with JWT + Neon DB per constitution |
| V. Security & Quality | PASS | JWT auth, input validation, user isolation, consistent responses |
| VI. Monorepo Structure | PASS | Backend in `/backend/` following web app structure |
| VII. Bonus Features | N/A | Core implementation phase |
| VIII. Deliverables | PASS | Clean commits, Task IDs in messages |
| IX. Violation Hierarchy | PASS | Following Constitution → Spec → Plan → Tasks |

## Project Structure

### Documentation (this feature)

```text
specs/001-fastapi-todo-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLModel engine + session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model (read-only, Better Auth)
│   │   └── task.py          # Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Request/Response Pydantic models
│   │   └── response.py      # Standard response wrappers
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (DB session, current user)
│   │   ├── auth.py          # Auth routes (/auth/*)
│   │   └── tasks.py         # Task CRUD routes (/tasks/*)
│   └── middleware/
│       ├── __init__.py
│       └── jwt.py           # JWT validation middleware
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_tasks.py        # Task CRUD tests
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Project metadata

frontend/                    # Existing Next.js frontend (unchanged)
├── lib/api.ts               # API client (target contract)
└── types/index.ts           # TypeScript interfaces (target contract)
```

**Structure Decision**: Web application structure with `/backend/` directory. Frontend already exists at `/frontend/`.

---

## 1. Architecture Overview

### FastAPI App Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI App                          │
├─────────────────────────────────────────────────────────────┤
│  Middleware Layer                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │    CORS     │  │   Logging   │  │  Exception Handler  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Route Layer                                                │
│  ┌─────────────────────┐  ┌────────────────────────────┐   │
│  │  /api/auth/*        │  │  /api/tasks/*              │   │
│  │  - POST /login      │  │  - GET    (list)           │   │
│  │  - POST /signup     │  │  - POST   (create)         │   │
│  │  - POST /logout     │  │  - GET    /{id}            │   │
│  └─────────────────────┘  │  - PUT    /{id}            │   │
│                           │  - DELETE /{id}            │   │
│                           └────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Dependency Layer                                           │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │  get_db()       │  │  get_current_user()             │  │
│  │  (DB Session)   │  │  (JWT → User extraction)        │  │
│  └─────────────────┘  └─────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SQLModel + Neon PostgreSQL                         │   │
│  │  - User table (managed by Better Auth)              │   │
│  │  - Task table (managed by this API)                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### JWT Middleware Flow

```
Request → CORS Check → JWT Extraction → Token Validation → User Resolution → Route Handler
                              │                 │                  │
                              ▼                 ▼                  ▼
                        Bearer token?     Valid signature?    User exists?
                              │                 │                  │
                              No → 401          No → 401          No → 401
```

### DB Session Dependency

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### CORS Configuration

```python
origins = [
    "http://localhost:3000",      # Next.js dev
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 2. Database Setup

### SQLModel Models

**User Model** (read-only, mirrors Better Auth):
```python
class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(primary_key=True)  # Better Auth generates UUID strings
    email: str = Field(unique=True, index=True)
    name: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="owner")
```

**Task Model**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "task"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key
    user_id: str = Field(foreign_key="user.id", index=True)

    # Relationship
    owner: User | None = Relationship(back_populates="tasks")
```

### Engine + Session

```python
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon connection string

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### Table Creation on Startup

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()
```

### Indexes

| Table | Column | Index Type | Rationale |
|-------|--------|------------|-----------|
| user | email | UNIQUE | Login lookup |
| task | user_id | B-TREE | Filter by owner |
| task | created_at | B-TREE | Sort by date |

---

## 3. JWT Authentication Middleware

### PyJWT Verification

```python
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

def verify_token(token: str) -> dict:
    """Verify JWT and return payload."""
    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### User ID Extraction

```python
async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate user from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    user_id = payload.get("sub") or payload.get("userId")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Fetch user from database
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

### Dependency for Routes

```python
# All task routes require authentication
router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("")
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskListResponse:
    ...
```

---

## 4. CRUD Routes Implementation Order

### Implementation Sequence

1. **POST /api/tasks** - Create task (foundational)
2. **GET /api/tasks** - List tasks (verify user isolation)
3. **GET /api/tasks/{id}** - Single task (ownership check)
4. **PUT /api/tasks/{id}** - Full update (title, description, completed)
5. **DELETE /api/tasks/{id}** - Remove task

### Route Signatures

```python
# 1. Create
@router.post("", status_code=201)
async def create_task(
    data: CreateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:

# 2. List
@router.get("")
async def list_tasks(
    completed: bool | None = Query(None),
    sort: str = Query("created_at"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskListResponse:

# 3. Get single
@router.get("/{task_id}")
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:

# 4. Update
@router.put("/{task_id}")
async def update_task(
    task_id: int,
    data: UpdateTaskRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:

# 5. Delete
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
```

### Ownership Enforcement Pattern

```python
async def get_task_by_id(
    task_id: int,
    user_id: str,
    db: AsyncSession,
) -> Task:
    """Get task ensuring ownership. Returns 404 for non-owned tasks."""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,  # User isolation at query level
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
```

---

## 5. Validation & Response Strategy

### Pydantic Request Schemas

```python
class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        return v

class UpdateTaskRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None
```

### Response Schemas (Match Frontend Types)

```python
class TaskSchema(BaseModel):
    id: str  # Convert int to string for frontend
    title: str
    description: str | None
    completed: bool
    createdAt: str  # ISO 8601
    updatedAt: str  # ISO 8601
    userId: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, task: Task) -> "TaskSchema":
        return cls(
            id=str(task.id),
            title=task.title,
            description=task.description,
            completed=task.completed,
            createdAt=task.created_at.isoformat(),
            updatedAt=task.updated_at.isoformat(),
            userId=task.user_id,
        )

class TaskResponse(BaseModel):
    task: TaskSchema

class TaskListResponse(BaseModel):
    tasks: list[TaskSchema]
    total: int
```

### Error Response Format

```python
class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    error: ErrorDetail

# Standard error codes
ERROR_CODES = {
    "VALIDATION_ERROR": "Input validation failed",
    "NOT_FOUND": "Resource not found",
    "UNAUTHORIZED": "Authentication required",
    "INVALID_CREDENTIALS": "Invalid email or password",
    "EMAIL_EXISTS": "Email already registered",
}
```

### Exception Handler

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc.errors()[0]["msg"]),
            }
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    code = "NOT_FOUND" if exc.status_code == 404 else "UNAUTHORIZED"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": exc.detail}},
    )
```

---

## 6. Environment & Integration

### Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
JWT_SECRET=your-better-auth-secret-here
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DEBUG=false
```

### Config Loading

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()
```

### Frontend Integration Points

| Frontend Call | Backend Endpoint | Method |
|---------------|------------------|--------|
| `api.auth.signup()` | `/api/auth/signup` | POST |
| `api.auth.login()` | `/api/auth/login` | POST |
| `api.auth.logout()` | `/api/auth/logout` | POST |
| `api.tasks.list()` | `/api/tasks` | GET |
| `api.tasks.create()` | `/api/tasks` | POST |
| `api.tasks.update()` | `/api/tasks/{id}` | PUT |
| `api.tasks.delete()` | `/api/tasks/{id}` | DELETE |

---

## 7. Testing & Verification Plan

### Key Test Flows

| Flow | Test Cases |
|------|------------|
| **Auth: Signup** | Valid signup, duplicate email, invalid email format |
| **Auth: Login** | Valid credentials, invalid password, non-existent user |
| **Task: Create** | Valid task, empty title, title too long, unauthenticated |
| **Task: List** | User's tasks only, empty list, filter by completed |
| **Task: Update** | Valid update, non-existent task, other user's task |
| **Task: Delete** | Valid delete, non-existent task, other user's task |
| **User Isolation** | User A cannot see/modify User B's tasks |

### Integration Test Structure

```python
# tests/test_tasks.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task_authenticated(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/tasks",
        json={"title": "Test Task"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["task"]["title"] == "Test Task"
    assert data["task"]["completed"] is False

@pytest.mark.asyncio
async def test_user_isolation(
    client: AsyncClient,
    user_a_headers: dict,
    user_b_headers: dict,
):
    # User A creates a task
    response = await client.post(
        "/api/tasks",
        json={"title": "User A's Task"},
        headers=user_a_headers,
    )
    task_id = response.json()["task"]["id"]

    # User B cannot see it
    response = await client.get(
        f"/api/tasks/{task_id}",
        headers=user_b_headers,
    )
    assert response.status_code == 404
```

### Frontend Integration Verification

1. Start backend: `uvicorn app.main:app --reload --port 8000`
2. Start frontend: `npm run dev` (port 3000)
3. Test signup flow → verify user created in DB
4. Test login flow → verify JWT returned and stored
5. Test task CRUD → verify operations work through UI
6. Test logout → verify token cleared

---

## Complexity Tracking

*No violations requiring justification.*

---

## Artifacts Generated

- [ ] `research.md` - Technology decisions and best practices
- [ ] `data-model.md` - SQLModel entity definitions
- [ ] `contracts/openapi.yaml` - API specification
- [ ] `quickstart.md` - Developer setup guide

---

**Plan complete. Next: Break into atomic speckit.tasks starting with database models and JWT middleware.**
