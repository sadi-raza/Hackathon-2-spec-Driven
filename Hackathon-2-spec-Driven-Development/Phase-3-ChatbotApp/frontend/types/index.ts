// Core Entities

export interface User {
  id: number;
  email: string;
  createdAt: string; // ISO 8601 date string
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: string; // ISO 8601 date string
  updatedAt: string; // ISO 8601 date string
  userId: number;
}

// For optimistic updates (before server assigns ID)
export interface OptimisticTask extends Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'> {
  tempId: string;
  isPending: boolean;
}

// API Response Types

export interface AuthResponse {
  user: User;
  token: string;
}

export interface AuthError {
  error: {
    code: 'INVALID_CREDENTIALS' | 'EMAIL_EXISTS' | 'VALIDATION_ERROR';
    message: string;
  };
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface TaskResponse {
  task: Task;
}

export interface TaskError {
  error: {
    code: 'NOT_FOUND' | 'UNAUTHORIZED' | 'VALIDATION_ERROR';
    message: string;
  };
}

export interface ApiError {
  error: {
    code: string;
    message: string;
  };
}

// UI State Types

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface AsyncState<T> {
  data: T | null;
  status: LoadingState;
  error: string | null;
}

export interface ModalState {
  isOpen: boolean;
  mode: 'create' | 'edit';
  task: Task | null;
}

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

// Theme Types

export type Theme = 'light' | 'dark' | 'system';

export interface ThemeState {
  theme: Theme;
  resolvedTheme: 'light' | 'dark';
}

// Query Keys
export const queryKeys = {
  tasks: ['tasks'] as const,
  task: (id: string) => ['tasks', id] as const,
  user: ['user'] as const,
} as const;

// Form Types (inferred from Zod schemas, but declared here for reference)
export interface LoginFormData {
  email: string;
  password: string;
}

export interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

export interface TaskFormData {
  title: string;
  description?: string | null;
}

// Task Create/Update payloads
export interface CreateTaskPayload {
  title: string;
  description?: string | null;
}

export interface UpdateTaskPayload {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

// Chat Types

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCallResult[];
  createdAt: string; // ISO 8601 date string
}

export interface ToolCallResult {
  tool: string;
  success: boolean;
  result?: string;
}

export interface ChatRequest {
  message: string;
  conversationId?: number;
}

export interface ChatResponse {
  conversationId: number;
  response: string;
  toolCalls: ToolCallResult[];
}

export interface Conversation {
  id: number;
  title: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}
