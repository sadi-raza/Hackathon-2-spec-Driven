'use client';

import { cn } from '@/lib/utils';

interface ChatLoadingProps {
  className?: string;
}

/**
 * Loading state indicator for chat messages.
 * Shows animated dots to indicate the assistant is typing.
 */
export function ChatLoading({ className }: ChatLoadingProps) {
  return (
    <div
      className={cn(
        'flex items-center gap-1 px-4 py-3 rounded-lg bg-muted max-w-[80%]',
        className
      )}
      role="status"
      aria-label="Assistant is typing"
    >
      <span className="sr-only">Assistant is typing...</span>
      <span
        className="h-2 w-2 rounded-full bg-muted-foreground/60 animate-bounce"
        style={{ animationDelay: '0ms' }}
      />
      <span
        className="h-2 w-2 rounded-full bg-muted-foreground/60 animate-bounce"
        style={{ animationDelay: '150ms' }}
      />
      <span
        className="h-2 w-2 rounded-full bg-muted-foreground/60 animate-bounce"
        style={{ animationDelay: '300ms' }}
      />
    </div>
  );
}
