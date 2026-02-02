'use client';

import { useState } from 'react';
import { Pencil, Trash2 } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { cn, formatDate } from '@/lib/utils';
import type { Task } from '@/types';

interface TaskCardProps {
  task: Task;
  onToggle: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  isToggling?: boolean;
}

export function TaskCard({
  task,
  onToggle,
  onEdit,
  onDelete,
  isToggling = false,
}: TaskCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const handleToggle = () => {
    onToggle(task.id, !task.completed);
  };

  return (
    <Card
      className={cn(
        'relative p-4 transition-all duration-200',
        task.completed && 'bg-muted/50',
        isToggling && 'opacity-70'
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <div className="pt-0.5">
          <Checkbox
            checked={task.completed}
            onCheckedChange={handleToggle}
            disabled={isToggling}
            aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={cn(
              'font-medium text-foreground truncate transition-all',
              task.completed && 'line-through text-muted-foreground'
            )}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={cn(
                'mt-1 text-sm text-muted-foreground line-clamp-2',
                task.completed && 'line-through'
              )}
            >
              {task.description}
            </p>
          )}

          <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
            <span>Created {formatDate(task.createdAt)}</span>
            {task.updatedAt !== task.createdAt && (
              <span className="text-muted-foreground/60">
                · Updated {formatDate(task.updatedAt)}
              </span>
            )}
          </div>
        </div>

        {/* Actions */}
        <div
          className={cn(
            'flex items-center gap-1 transition-opacity',
            isHovered ? 'opacity-100' : 'opacity-0 sm:opacity-100'
          )}
        >
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit(task)}
            title="Edit task"
            className="h-8 w-8"
          >
            <Pencil className="h-4 w-4" />
            <span className="sr-only">Edit</span>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(task)}
            title="Delete task"
            className="h-8 w-8 text-destructive hover:text-destructive"
          >
            <Trash2 className="h-4 w-4" />
            <span className="sr-only">Delete</span>
          </Button>
        </div>
      </div>

      {/* Status indicator */}
      <div
        className={cn(
          'absolute left-0 top-0 bottom-0 w-1 rounded-l-lg transition-colors',
          task.completed ? 'bg-green-500' : 'bg-primary'
        )}
      />
    </Card>
  );
}
