'use client';

import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '@/components/ui/modal';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { taskSchema } from '@/validations/schemas';
import { useCreateTask, useUpdateTask } from '@/hooks/useTasks';
import type { Task } from '@/types';

// Form input type (before Zod transformation)
interface TaskFormInput {
  title: string;
  description?: string;
}

// Output type after Zod transformation
type TaskFormOutput = z.output<typeof taskSchema>;

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task?: Task | null;
}

export function TaskModal({ isOpen, onClose, task }: TaskModalProps) {
  const isEditing = !!task;
  const createTask = useCreateTask();
  const updateTask = useUpdateTask();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TaskFormInput, unknown, TaskFormOutput>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
    },
  });

  // Reset form when modal opens/closes or task changes
  useEffect(() => {
    if (isOpen) {
      reset({
        title: task?.title ?? '',
        description: task?.description ?? '',
      });
    }
  }, [isOpen, task, reset]);

  const onSubmit = async (data: TaskFormOutput) => {
    try {
      if (isEditing && task) {
        await updateTask.mutateAsync({
          id: task.id,
          data: {
            title: data.title,
            description: data.description || null,
          },
        });
      } else {
        await createTask.mutateAsync({
          title: data.title,
          description: data.description || null,
        });
      }
      onClose();
    } catch {
      // Error is handled in mutation hooks
    }
  };

  const isPending = createTask.isPending || updateTask.isPending;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEditing ? 'Edit Task' : 'Create Task'}
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="title" className="text-sm font-medium text-foreground">
            Title <span className="text-destructive">*</span>
          </label>
          <Input
            id="title"
            placeholder="Enter task title"
            error={!!errors.title}
            disabled={isPending}
            {...register('title')}
          />
          {errors.title && (
            <p className="text-sm text-destructive">{errors.title.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="description" className="text-sm font-medium text-foreground">
            Description <span className="text-muted-foreground">(optional)</span>
          </label>
          <textarea
            id="description"
            placeholder="Enter task description"
            disabled={isPending}
            className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            {...register('description')}
          />
          {errors.description && (
            <p className="text-sm text-destructive">{errors.description.message}</p>
          )}
        </div>

        <div className="flex justify-end gap-2 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={isPending}
          >
            Cancel
          </Button>
          <Button type="submit" isLoading={isPending}>
            {isEditing ? 'Save Changes' : 'Create Task'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
