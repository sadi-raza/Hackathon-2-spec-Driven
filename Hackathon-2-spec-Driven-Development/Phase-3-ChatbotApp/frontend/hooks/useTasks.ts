'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { api, ApiError } from '@/lib/api';
import type { Task, CreateTaskPayload, UpdateTaskPayload, TaskListResponse } from '@/types';

// Query keys for cache management
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: () => [...taskKeys.lists()] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
};

// Fetch all tasks for the authenticated user
export function useTasks() {
  return useQuery({
    queryKey: taskKeys.list(),
    queryFn: async () => {
      const response = await api.tasks.list();
      return response;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

// Create a new task with optimistic updates
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateTaskPayload) => api.tasks.create(data),
    onMutate: async (newTask) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskKeys.list() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<TaskListResponse>(taskKeys.list());

      // Optimistically add new task
      if (previousTasks) {
        const optimisticTask: Task = {
          id: `temp-${Date.now()}`,
          title: newTask.title,
          description: newTask.description ?? null,
          completed: false,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          userId: 'temp',
        };

        queryClient.setQueryData<TaskListResponse>(taskKeys.list(), {
          tasks: [...previousTasks.tasks, optimisticTask],
          total: previousTasks.total + 1,
        });
      }

      return { previousTasks };
    },
    onError: (error, _newTask, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list(), context.previousTasks);
      }

      if (error instanceof ApiError) {
        toast.error(error.message);
      } else {
        toast.error('Failed to create task. Please try again.');
      }
    },
    onSuccess: () => {
      toast.success('Task created successfully!');
    },
    onSettled: () => {
      // Refetch after mutation to ensure sync with server
      queryClient.invalidateQueries({ queryKey: taskKeys.list() });
    },
  });
}

// Update an existing task with optimistic updates
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateTaskPayload }) =>
      api.tasks.update(id, data),
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.list() });

      const previousTasks = queryClient.getQueryData<TaskListResponse>(taskKeys.list());

      if (previousTasks) {
        const updatedTasks = previousTasks.tasks.map((task) =>
          task.id === id
            ? { ...task, ...data, updatedAt: new Date().toISOString() }
            : task
        );

        queryClient.setQueryData<TaskListResponse>(taskKeys.list(), {
          tasks: updatedTasks,
          total: previousTasks.total,
        });
      }

      return { previousTasks };
    },
    onError: (error, _variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list(), context.previousTasks);
      }

      if (error instanceof ApiError) {
        toast.error(error.message);
      } else {
        toast.error('Failed to update task. Please try again.');
      }
    },
    onSuccess: () => {
      toast.success('Task updated successfully!');
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.list() });
    },
  });
}

// Toggle task completion status with optimistic updates
export function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, completed }: { id: string; completed: boolean }) =>
      api.tasks.update(id, { completed }),
    onMutate: async ({ id, completed }) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.list() });

      const previousTasks = queryClient.getQueryData<TaskListResponse>(taskKeys.list());

      if (previousTasks) {
        const updatedTasks = previousTasks.tasks.map((task) =>
          task.id === id
            ? { ...task, completed, updatedAt: new Date().toISOString() }
            : task
        );

        queryClient.setQueryData<TaskListResponse>(taskKeys.list(), {
          tasks: updatedTasks,
          total: previousTasks.total,
        });
      }

      return { previousTasks };
    },
    onError: (error, _variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list(), context.previousTasks);
      }

      if (error instanceof ApiError) {
        toast.error(error.message);
      } else {
        toast.error('Failed to update task. Please try again.');
      }
    },
    // No success toast for toggle - visual change is enough
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.list() });
    },
  });
}

// Delete a task with optimistic updates
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.tasks.delete(id),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.list() });

      const previousTasks = queryClient.getQueryData<TaskListResponse>(taskKeys.list());

      if (previousTasks) {
        const filteredTasks = previousTasks.tasks.filter((task) => task.id !== id);

        queryClient.setQueryData<TaskListResponse>(taskKeys.list(), {
          tasks: filteredTasks,
          total: previousTasks.total - 1,
        });
      }

      return { previousTasks };
    },
    onError: (error, _id, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list(), context.previousTasks);
      }

      if (error instanceof ApiError) {
        toast.error(error.message);
      } else {
        toast.error('Failed to delete task. Please try again.');
      }
    },
    onSuccess: () => {
      toast.success('Task deleted successfully!');
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.list() });
    },
  });
}
