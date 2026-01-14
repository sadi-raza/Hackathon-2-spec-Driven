# Quickstart: FastAPI Todo API Backend

**Feature**: `001-fastapi-todo-api`
**Date**: 2026-01-09

Get the backend running in under 5 minutes.

---

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database (or local PostgreSQL)
- Node.js 18+ (for frontend)

---

## 1. Setup Backend

```bash
# Navigate to project root
cd Phase-2-Full-Stack-Todo-App

# Create backend directory
mkdir -p backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### requirements.txt

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlmodel>=0.0.14
asyncpg>=0.29.0
pyjwt>=2.8.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0
pydantic-settings>=2.1.0
httpx>=0.26.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

---

## 2. Configure Environment

Create `.env` file in `/backend/`:

```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/dbname?sslmode=require

# JWT Secret (MUST match frontend's Better Auth secret)
JWT_SECRET=your-better-auth-secret-here

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Debug mode
DEBUG=false
```

### Get Neon Database URL

1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Replace `postgresql://` with `postgresql+asyncpg://`

---

## 3. Run Backend

```bash
# From /backend directory
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# Expected response
{"status": "healthy"}
```

---

## 4. Run Frontend

In a new terminal:

```bash
# From project root
cd frontend

# Install dependencies (if not done)
npm install

# Create .env.local
cp .env.example .env.local

# Edit .env.local with same JWT secret
# BETTER_AUTH_SECRET=your-better-auth-secret-here

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 5. Test Integration

1. Open `http://localhost:3000` in browser
2. Sign up for a new account
3. Create a task
4. Verify task appears in the list
5. Toggle completion status
6. Delete task

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| POST | `/api/auth/logout` | Clear session |
| GET | `/api/tasks` | List user's tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get single task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |

---

## Project Structure

```
Phase-2-Full-Stack-Todo-App/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py        # Settings
│   │   ├── database.py      # DB connection
│   │   ├── models/          # SQLModel entities
│   │   ├── schemas/         # Pydantic models
│   │   ├── api/             # Route handlers
│   │   └── middleware/      # JWT auth
│   ├── tests/
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── lib/                 # API client
│   └── types/               # TypeScript types
└── specs/
    └── 001-fastapi-todo-api/
```

---

## Common Issues

### CORS Error
- Check `CORS_ORIGINS` in backend `.env`
- Ensure frontend URL matches exactly

### JWT Invalid
- Verify `JWT_SECRET` matches in both frontend and backend
- Check token expiration

### Database Connection
- Ensure Neon project is active
- Check connection string format includes `asyncpg`
- Verify SSL mode is set

### Module Not Found
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

---

## Development Commands

```bash
# Backend
uvicorn app.main:app --reload --port 8000    # Start dev server
pytest                                        # Run tests
pytest -v --cov=app                          # Tests with coverage

# Frontend
npm run dev      # Start dev server
npm run build    # Production build
npm run lint     # Lint code
```

---

## Next Steps

After setup:
1. Review `specs/001-fastapi-todo-api/spec.md` for requirements
2. Check `specs/001-fastapi-todo-api/plan.md` for implementation details
3. Run `tasks.md` tasks sequentially (after generation)
