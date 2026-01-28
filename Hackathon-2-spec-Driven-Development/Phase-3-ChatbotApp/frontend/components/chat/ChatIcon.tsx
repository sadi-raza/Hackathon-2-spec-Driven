'use client';

import { MessageCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface ChatIconProps {
  onClick: () => void;
  isOpen?: boolean;
  hasUnread?: boolean;
  className?: string;
}

/**
 * Floating chat icon button for opening the chatbot modal.
 * Appears in the bottom-right corner of the dashboard.
 */
export function ChatIcon({ onClick, isOpen, hasUnread, className }: ChatIconProps) {
  return (
    <Button
      variant="default"
      size="icon"
      onClick={onClick}
      aria-label={isOpen ? 'Close chat' : 'Open chat assistant'}
      aria-expanded={isOpen}
      className={cn(
        'fixed bottom-6 right-6 z-40 h-14 w-14 rounded-full shadow-lg',
        'hover:scale-105 transition-transform duration-200',
        'focus-visible:ring-offset-4',
        isOpen && 'bg-secondary text-secondary-foreground',
        className
      )}
    >
      <MessageCircle className={cn('h-6 w-6', isOpen && 'rotate-180')} />

      {/* Unread indicator */}
      {hasUnread && !isOpen && (
        <span
          className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-destructive"
          aria-hidden="true"
        />
      )}
    </Button>
  );
}
