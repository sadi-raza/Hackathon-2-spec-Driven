import type {
  AuthResponse,
  TaskListResponse,
  TaskResponse,
  CreateTaskPayload,
  UpdateTaskPayload,
} from '@/types';
import { getToken, clearAuth } from './auth';

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  'https://developer-2526-fastapi-todo-app.hf.space/api';

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = getToken();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle 401 - redirect to login
    if (response.status === 401) {
      clearAuth();
      if (typeof window !== 'undefined') {
        window.location.href = '/login?session=expired';
      }
      throw new ApiError('UNAUTHORIZED', 'Session expired');
    }

    const data = await response.json();

    if (!response.ok) {
      const error = data.error || { code: 'UNKNOWN_ERROR', message: 'An error occurred' };
      throw new ApiError(error.code, error.message);
    }

    return data as T;
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

    create: (data: CreateTaskPayload) =>
      this.request<TaskResponse>('/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    update: (id: string, data: UpdateTaskPayload) =>
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
