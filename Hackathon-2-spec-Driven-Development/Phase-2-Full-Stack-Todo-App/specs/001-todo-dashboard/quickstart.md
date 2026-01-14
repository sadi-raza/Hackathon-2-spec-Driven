# Quickstart: Phase II Todo Dashboard Frontend

**Feature**: 001-todo-dashboard
**Date**: 2025-01-08

## Prerequisites

- Node.js 20+ (LTS)
- pnpm 9+ (or npm/yarn)
- Backend API running on `http://localhost:8000` (or configure `NEXT_PUBLIC_API_URL`)

## Quick Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env.local

# Start development server
pnpm dev
```

## Environment Variables

Create `frontend/.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Auth Configuration (Better Auth)
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

## Project Structure After Implementation

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout with providers
│   ├── page.tsx             # Landing/redirect
│   ├── global-error.tsx     # Global error boundary
│   ├── not-found.tsx        # 404 page
│   ├── (auth)/
│   │   ├── login/page.tsx   # Login page
│   │   └── signup/page.tsx  # Signup page
│   └── (protected)/
│       ├── layout.tsx       # Protected layout with auth check
│       └── dashboard/
│           ├── page.tsx     # Dashboard page
│           ├── loading.tsx  # Loading skeleton
│           └── error.tsx    # Dashboard error boundary
├── components/
│   ├── ui/                  # Base UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── modal.tsx
│   │   ├── card.tsx
│   │   └── skeleton.tsx
│   ├── Header.tsx           # App header with nav
│   ├── ThemeToggle.tsx      # Dark/light mode toggle
│   ├── TaskList.tsx         # Task list container
│   ├── TaskCard.tsx         # Mobile task card
│   ├── TaskTable.tsx        # Desktop task table
│   ├── TaskModal.tsx        # Create/edit modal
│   ├── EmptyState.tsx       # No tasks state
│   ├── ConfirmDialog.tsx    # Delete confirmation
│   └── ToastProvider.tsx    # Toast notifications
├── lib/
│   ├── api.ts               # API client
│   ├── auth.ts              # Auth utilities
│   ├── utils.ts             # Helper functions
│   └── validations.ts       # Zod schemas
├── hooks/
│   ├── useTasks.ts          # Task CRUD hooks
│   ├── useAuth.ts           # Auth hooks
│   └── useTheme.ts          # Theme hook
├── types/
│   └── index.ts             # TypeScript types
└── styles/
    └── globals.css          # Tailwind + custom styles
```

## Key Commands

```bash
# Development
pnpm dev          # Start dev server (http://localhost:3000)

# Build
pnpm build        # Production build
pnpm start        # Start production server

# Quality
pnpm lint         # Run ESLint
pnpm typecheck    # TypeScript check

# Testing (if added)
pnpm test         # Run tests
```

## Development Workflow

1. **Start Backend**: Ensure FastAPI backend is running on port 8000
2. **Start Frontend**: Run `pnpm dev`
3. **Test Auth Flow**: Create account, login, logout
4. **Test Task CRUD**: Create, view, edit, toggle, delete tasks
5. **Test Responsive**: Check mobile (cards) and desktop (table) views
6. **Test Dark Mode**: Toggle theme, check system preference

## Key Features to Verify

| Feature | URL | Expected Behavior |
|---------|-----|-------------------|
| Login | `/login` | Form with validation, redirect to dashboard |
| Signup | `/signup` | Form with password rules, redirect to dashboard |
| Dashboard | `/dashboard` | Task list with CRUD operations |
| Protected Routes | `/dashboard` (not logged in) | Redirect to `/login` |
| Dark Mode | Header toggle | Theme switches, persists |
| Error Handling | Any error | Friendly message, no stack trace |

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check JWT token in cookies/localStorage
2. **CORS Errors**: Verify backend allows frontend origin
3. **Type Errors**: Run `pnpm typecheck` to identify issues
4. **Styling Issues**: Check Tailwind config and class names

### Debug Mode

Add to `.env.local`:
```env
NEXT_PUBLIC_DEBUG=true
```

This enables console logging for API calls and state changes.
