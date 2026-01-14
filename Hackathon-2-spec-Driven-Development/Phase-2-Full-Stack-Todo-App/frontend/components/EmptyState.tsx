'use client';

import { ClipboardList, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  onCreateFirst: () => void;
}

export function EmptyState({ onCreateFirst }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="relative mb-6">
        <div className="flex h-24 w-24 items-center justify-center rounded-full bg-primary/10">
          <ClipboardList className="h-12 w-12 text-primary" />
        </div>
        <div className="absolute -bottom-1 -right-1 flex h-8 w-8 items-center justify-center rounded-full bg-muted">
          <span className="text-lg">0</span>
        </div>
      </div>

      <h3 className="mb-2 text-xl font-semibold text-foreground">No tasks yet</h3>
      <p className="mb-6 max-w-sm text-center text-muted-foreground">
        Get started by creating your first task. Stay organized and track your
        progress with ease.
      </p>

      <Button onClick={onCreateFirst} className="gap-2">
        <Plus className="h-4 w-4" />
        Create your first task
      </Button>
    </div>
  );
}
