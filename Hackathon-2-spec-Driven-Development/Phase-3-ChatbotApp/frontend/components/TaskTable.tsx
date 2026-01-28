'use client';

import { Pencil, Trash2 } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { cn, formatDate } from '@/lib/utils';
import type { Task } from '@/types';

interface TaskTableProps {
  tasks: Task[];
  onToggle: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  togglingId?: string;
}

export function TaskTable({
  tasks,
  onToggle,
  onEdit,
  onDelete,
  togglingId,
}: TaskTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <table className="w-full">
        <thead className="bg-muted/50">
          <tr>
            <th className="w-12 px-4 py-3 text-left">
              <span className="sr-only">Status</span>
            </th>
            <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
              Title
            </th>
            <th className="hidden px-4 py-3 text-left text-sm font-medium text-muted-foreground lg:table-cell">
              Description
            </th>
            <th className="hidden px-4 py-3 text-left text-sm font-medium text-muted-foreground md:table-cell">
              Created
            </th>
            <th className="w-24 px-4 py-3 text-right text-sm font-medium text-muted-foreground">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {tasks.map((task) => (
            <tr
              key={task.id}
              className={cn(
                'group transition-colors hover:bg-muted/30',
                task.completed && 'bg-muted/20',
                togglingId === task.id && 'opacity-70'
              )}
            >
              {/* Checkbox */}
              <td className="px-4 py-3">
                <Checkbox
                  checked={task.completed}
                  onCheckedChange={() => onToggle(task.id, !task.completed)}
                  disabled={togglingId === task.id}
                  aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
                />
              </td>

              {/* Title */}
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      'font-medium text-foreground truncate max-w-xs',
                      task.completed && 'line-through text-muted-foreground'
                    )}
                  >
                    {task.title}
                  </span>
                  {task.completed && (
                    <span className="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/30 px-2 py-0.5 text-xs font-medium text-green-700 dark:text-green-400">
                      Done
                    </span>
                  )}
                </div>
              </td>

              {/* Description */}
              <td className="hidden px-4 py-3 lg:table-cell">
                <span
                  className={cn(
                    'text-sm text-muted-foreground truncate block max-w-md',
                    task.completed && 'line-through'
                  )}
                >
                  {task.description || '—'}
                </span>
              </td>

              {/* Created Date */}
              <td className="hidden px-4 py-3 md:table-cell">
                <span className="text-sm text-muted-foreground">
                  {formatDate(task.createdAt)}
                </span>
              </td>

              {/* Actions */}
              <td className="px-4 py-3 text-right">
                <div className="flex items-center justify-end gap-1 opacity-0 transition-opacity group-hover:opacity-100 focus-within:opacity-100">
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
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
