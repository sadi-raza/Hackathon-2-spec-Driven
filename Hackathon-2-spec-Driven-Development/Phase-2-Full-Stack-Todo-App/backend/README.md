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