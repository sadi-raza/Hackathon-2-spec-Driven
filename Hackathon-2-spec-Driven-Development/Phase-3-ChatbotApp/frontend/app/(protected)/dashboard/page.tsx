'use client';

import { useState } from 'react';
import { Plus } from 'lucide-react';
import { useTasks, useToggleTask, useDeleteTask } from '@/hooks/useTasks';
import { TaskList } from '@/components/TaskList';
import { TaskModal } from '@/components/TaskModal';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { ChatIcon, ChatModal } from '@/components/chat';
import { Button } from '@/components/ui/button';
import type { Task } from '@/types';

// Check if chatbot feature is enabled via environment variable
const CHATBOT_ENABLED = process.env.NEXT_PUBLIC_CHATBOT_ENABLED === 'true';

export default function DashboardPage() {
  const { data, isLoading } = useTasks();
  const toggleTask = useToggleTask();
  const deleteTask = useDeleteTask();

  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Delete confirmation state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);

  // Chat modal state
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Currently toggling task ID for loading state
  const [togglingId, setTogglingId] = useState<string | undefined>();

  const tasks = data?.tasks ?? [];

  const handleCreateTask = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleToggleTask = async (id: string, completed: boolean) => {
    setTogglingId(id);
    try {
      await toggleTask.mutateAsync({ id: Number(id), completed });
    } finally {
      setTogglingId(undefined);
    }
  };

  const handleDeleteClick = (task: Task) => {
    setTaskToDelete(task);
    setDeleteConfirmOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (taskToDelete) {
      await deleteTask.mutateAsync(taskToDelete.id);
      setDeleteConfirmOpen(false);
      setTaskToDelete(null);
    }
  };

  const handleCancelDelete = () => {
    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setEditingTask(null);
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">My Tasks</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {isLoading
              ? 'Loading tasks...'
              : `${tasks.length} task${tasks.length === 1 ? '' : 's'}`}
          </p>
        </div>

        <Button onClick={handleCreateTask} className="gap-2">
          <Plus className="h-4 w-4" />
          <span className="hidden sm:inline">Add Task</span>
        </Button>
      </div>

      {/* Task list */}
      <TaskList
        tasks={tasks}
        isLoading={isLoading}
        onToggle={handleToggleTask}
        onEdit={handleEditTask}
        onDelete={handleDeleteClick}
        onCreateFirst={handleCreateTask}
        togglingId={togglingId}
      />

      {/* Create/Edit Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        task={editingTask}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        title="Delete Task"
        description={`Are you sure you want to delete "${taskToDelete?.title}"? This action cannot be undone.`}
        confirmLabel="Delete"
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        isLoading={deleteTask.isPending}
        variant="destructive"
      />

      {/* Chat components (conditionally rendered based on feature flag) */}
      {CHATBOT_ENABLED && (
        <>
          <ChatIcon
            onClick={() => setIsChatOpen(!isChatOpen)}
            isOpen={isChatOpen}
          />
          <ChatModal
            isOpen={isChatOpen}
            onClose={() => setIsChatOpen(false)}
          />
        </>
      )}
    </div>
  );
}
