'use client';

import { Toaster } from 'sonner';

export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        classNames: {
          toast:
            'bg-card text-card-foreground border-border shadow-lg rounded-lg px-4 py-3',
          title: 'font-medium',
          description: 'text-muted-foreground text-sm',
          success: 'border-l-4 border-l-success',
          error: 'border-l-4 border-l-destructive',
          warning: 'border-l-4 border-l-warning',
          info: 'border-l-4 border-l-primary',
        },
      }}
      closeButton
      richColors
    />
  );
}
