'use client';

import { useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { ChatLoading } from './ChatLoading';
import type { ChatMessage, ToolCallResult } from '@/types';

interface ChatMessagesProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  className?: string;
}

/**
 * Displays the list of chat messages with proper formatting.
 * Auto-scrolls to the latest message.
 */
export function ChatMessages({ messages, isLoading, className }: ChatMessagesProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className={cn('flex flex-1 items-center justify-center p-4', className)}>
        <div className="text-center text-muted-foreground">
          <p className="text-sm">No messages yet.</p>
          <p className="mt-1 text-xs">
            Try saying &quot;Add buy milk&quot; or &quot;Show my tasks&quot;
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('flex flex-1 flex-col gap-3 overflow-y-auto p-4', className)}>
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {isLoading && <ChatLoading />}

      <div ref={messagesEndRef} />
    </div>
  );
}

interface MessageBubbleProps {
  message: ChatMessage;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex flex-col gap-1',
        isUser ? 'items-end' : 'items-start'
      )}
    >
      <div
        className={cn(
          'max-w-[80%] rounded-lg px-4 py-2',
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>

      {/* Show tool calls if present (assistant messages) */}
      {!isUser && message.toolCalls && message.toolCalls.length > 0 && (
        <ToolCallsDisplay toolCalls={message.toolCalls} />
      )}

      <span className="text-xs text-muted-foreground">
        {formatMessageTime(message.createdAt)}
      </span>
    </div>
  );
}

interface ToolCallsDisplayProps {
  toolCalls: ToolCallResult[];
}

function ToolCallsDisplay({ toolCalls }: ToolCallsDisplayProps) {
  return (
    <div className="flex flex-col gap-1 max-w-[80%]">
      {toolCalls.map((toolCall, index) => (
        <div
          key={index}
          className={cn(
            'text-xs px-3 py-1.5 rounded border',
            toolCall.success
              ? 'bg-green-50 border-green-200 text-green-700 dark:bg-green-950 dark:border-green-800 dark:text-green-300'
              : 'bg-red-50 border-red-200 text-red-700 dark:bg-red-950 dark:border-red-800 dark:text-red-300'
          )}
        >
          <span className="font-medium">{toolCall.tool}</span>
          {toolCall.result && (
            <span className="ml-1">: {toolCall.result}</span>
          )}
        </div>
      ))}
    </div>
  );
}

function formatMessageTime(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(date);
}
