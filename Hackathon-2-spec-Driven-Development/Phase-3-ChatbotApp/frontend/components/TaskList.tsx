'use client';
import { TaskCard } from '@/components/TaskCard';
import { TaskTable } from '@/components/TaskTable';
import { EmptyState } from '@/components/EmptyState';
import { TaskListSkeleton } from '@/components/ui/skeleton';
import type { Task } from '@/types';

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onToggle: (id: number, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  onCreateFirst: () => void;
  togglingId?: number;
}

export function TaskList({
  tasks,
  isLoading,
  onToggle,
  onEdit,
  onDelete,
  onCreateFirst,
  togglingId,
}: TaskListProps) {
  // Show loading skeleton
  if (isLoading) {
    return <TaskListSkeleton />;
  }

  // Show empty state if no tasks
  if (tasks.length === 0) {
    return <EmptyState onCreateFirst={onCreateFirst} />;
  }

  return (
    <>
      {/* Mobile: Card view */}
      <div className="block md:hidden space-y-3">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onToggle={onToggle}
            onEdit={onEdit}
            onDelete={onDelete}
            isToggling={togglingId === task.id}
          />
        ))}
      </div>

      {/* Desktop: Table view */}
      <div className="hidden md:block">
        <TaskTable
          tasks={tasks}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
          togglingId={togglingId}
        />
      </div>
    </>
  );
}
