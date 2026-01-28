# Research: Phase II Todo Dashboard Frontend

**Feature**: 001-todo-dashboard
**Date**: 2025-01-08
**Status**: Complete

## Technology Decisions

### 1. Next.js Version & App Router Strategy

**Decision**: Next.js 15.1+ with App Router (latest stable as of January 2026)

**Rationale**:
- App Router provides Server Components by default for optimal performance
- Built-in layouts, loading states, and error boundaries align with spec requirements
- Server Actions available for form submissions (though we'll use client-side for optimistic updates)
- Excellent TypeScript support with strict mode

**Alternatives Considered**:
- Next.js Pages Router: Rejected - legacy approach, less aligned with 2026 standards
- Remix: Rejected - smaller ecosystem, less suitable for hackathon timeline
- Vite + React: Rejected - requires more boilerplate, no built-in SSR patterns

### 2. Authentication Strategy

**Decision**: Better Auth with JWT tokens stored in httpOnly cookies

**Rationale**:
- Better Auth is the specified authentication library per constitution (Phase II)
- JWT tokens provide stateless authentication
- httpOnly cookies prevent XSS token theft
- Works seamlessly with Next.js middleware for route protection

**Alternatives Considered**:
- NextAuth.js: Rejected - Better Auth specified in constitution
- Custom JWT implementation: Rejected - unnecessary complexity
- Session-based auth: Rejected - JWT required per constitution

### 3. State Management Approach

**Decision**: React Server Components + Client Components with React Query (TanStack Query) for data fetching

**Rationale**:
- Server Components for initial data fetch (dashboard load)
- React Query provides caching, optimistic updates, and rollback out-of-box
- Minimal client-side state needed (form state handled by react-hook-form)
- Aligns with Next.js 15 best practices

**Alternatives Considered**:
- Zustand: Rejected - overkill for this scope, React Query handles data state
- Redux: Rejected - too much boilerplate, not needed
- SWR: Viable alternative but React Query has better optimistic update API

### 4. Styling Approach

**Decision**: Tailwind CSS v4 with custom design tokens inspired by shadcn/ui

**Rationale**:
- Tailwind v4 provides container queries and modern utilities
- shadcn/ui patterns are accessible and production-ready
- No external component library dependency - components built with Tailwind
- CSS variables for dark/light mode theming

**Alternatives Considered**:
- Styled Components: Rejected - runtime overhead, not aligned with Server Components
- CSS Modules: Rejected - more verbose, less consistent
- Full shadcn/ui installation: Rejected - only need patterns, not full library

### 5. Form Validation

**Decision**: Zod + react-hook-form

**Rationale**:
- Zod provides runtime type validation with TypeScript inference
- react-hook-form is performant and integrates well with Zod
- Real-time validation matches spec requirements (FR-020)
- Server-side validation can reuse Zod schemas

**Alternatives Considered**:
- Yup: Rejected - Zod has better TypeScript integration
- Formik: Rejected - heavier, less performant than react-hook-form

### 6. Toast Notifications

**Decision**: Sonner toast library

**Rationale**:
- Lightweight, accessible, and beautiful by default
- Supports promise-based toasts for async operations
- Works well with Server Components
- Minimal configuration needed

**Alternatives Considered**:
- React Hot Toast: Viable but Sonner has better defaults
- Custom implementation: Rejected - unnecessary effort

### 7. Dark Mode Implementation

**Decision**: next-themes with CSS variables

**Rationale**:
- Handles system preference detection automatically
- Prevents flash of incorrect theme on load
- Simple API for manual toggle
- Works with Tailwind's dark mode

**Alternatives Considered**:
- Custom implementation: Rejected - next-themes solves edge cases
- Tailwind's built-in dark mode only: Insufficient - no system preference detection

## API Integration Research

### Backend API Contract (Assumed)

Based on spec assumptions, the frontend will integrate with:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/signup` | POST | Create new user account |
| `/api/auth/login` | POST | Authenticate and receive JWT |
| `/api/auth/logout` | POST | Invalidate session |
| `/api/tasks` | GET | Fetch all tasks for authenticated user |
| `/api/tasks` | POST | Create new task |
| `/api/tasks/:id` | PUT | Update existing task |
| `/api/tasks/:id` | DELETE | Delete task |

### Error Response Format (Assumed)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message here",
    "details": {}
  }
}
```

## Performance Research

### Loading Strategy

**Decision**: Streaming with Suspense boundaries

- Initial page shell renders immediately
- Task data streams in with loading skeletons
- Error boundaries catch failures at appropriate levels

### Optimistic Update Pattern

```typescript
// Pattern for task operations
const createTask = useMutation({
  mutationFn: api.tasks.create,
  onMutate: async (newTask) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['tasks'] })
    // Snapshot previous value
    const previous = queryClient.getQueryData(['tasks'])
    // Optimistically update
    queryClient.setQueryData(['tasks'], (old) => [...old, { ...newTask, id: 'temp' }])
    return { previous }
  },
  onError: (err, newTask, context) => {
    // Rollback on error
    queryClient.setQueryData(['tasks'], context.previous)
    toast.error('Failed to create task')
  },
  onSuccess: () => {
    toast.success('Task created')
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks'] })
  }
})
```

## Responsive Design Research

### Breakpoint Strategy

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 768px | Card-based task list |
| Tablet | 768px - 1024px | Hybrid (cards with more info) |
| Desktop | >= 1024px | Table-based task list |

### Component Switching Pattern

```typescript
// Using Tailwind's responsive utilities
<div className="block md:hidden">
  <TaskCards tasks={tasks} />
</div>
<div className="hidden md:block">
  <TaskTable tasks={tasks} />
</div>
```

## Error Handling Research

### Error Boundary Hierarchy

1. **Root**: `app/global-error.tsx` - Catches unhandled errors app-wide
2. **Layout**: `app/dashboard/error.tsx` - Catches dashboard-specific errors
3. **Component**: Try-catch in async operations with toast feedback

### 401 Handling Pattern

```typescript
// In API client
if (response.status === 401) {
  // Clear local auth state
  // Redirect to login
  window.location.href = '/login?session=expired'
}
```

## Accessibility Research

### WCAG 2.1 AA Compliance Targets

- Color contrast ratio: minimum 4.5:1 for text
- Focus indicators: visible on all interactive elements
- Keyboard navigation: all features accessible via keyboard
- Screen reader support: proper ARIA labels and roles

## Conclusions

All technical decisions are resolved. No NEEDS CLARIFICATION items remain. The frontend can proceed with implementation using:

- **Framework**: Next.js 15.1+ with App Router
- **Auth**: Better Auth with JWT
- **State**: React Query for data, react-hook-form for forms
- **Styling**: Tailwind CSS v4 with shadcn/ui patterns
- **Validation**: Zod
- **Toasts**: Sonner
- **Dark Mode**: next-themes
