'use client';

import { useState, useRef, useCallback, useEffect, type FormEvent } from 'react';
import { X, Send } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ChatMessages } from './ChatMessages';
import { chatApi, generateMessageId, ChatApiError } from '@/lib/chat-api';
import type { ChatMessage } from '@/types';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

/**
 * Chat modal panel for interacting with the AI assistant.
 * Handles message sending, loading states, and conversation persistence.
 */
export function ChatModal({ isOpen, onClose, className }: ChatModalProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  // Handle escape key to close
  const handleEscape = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    },
    [onClose]
  );

  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      // Focus input when modal opens
      setTimeout(() => inputRef.current?.focus(), 100);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, handleEscape]);

  // Load existing conversation on mount if we have a conversation ID
  useEffect(() => {
    if (isOpen && conversationId) {
      loadConversation(conversationId);
    }
  }, [isOpen, conversationId]);

  const loadConversation = async (convId: number) => {
    try {
      const data = await chatApi.getConversationMessages(convId);
      setMessages(data.messages);
    } catch (err) {
      // Ignore errors loading conversation - start fresh
      console.warn('Failed to load conversation:', err);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const message = inputValue.trim();
    if (!message || isLoading) return;

    setError(null);

    // Add user message optimistically
    const userMessage: ChatMessage = {
      id: generateMessageId(),
      role: 'user',
      content: message,
      createdAt: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await chatApi.sendMessage({
        message,
        conversationId: conversationId ?? undefined,
      });

      // Update conversation ID if this is a new conversation
      if (!conversationId) {
        setConversationId(response.conversationId);
      }

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: generateMessageId(),
        role: 'assistant',
        content: response.response,
        toolCalls: response.toolCalls,
        createdAt: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      // Show error message
      const errorMessage =
        err instanceof ChatApiError
          ? err.message
          : 'Something went wrong. Please try again.';

      setError(errorMessage);

      // Remove the optimistic user message on error
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
      setInputValue(message); // Restore the input
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    inputRef.current?.focus();
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="chat-title"
      className={cn(
        'fixed bottom-24 right-6 z-50 flex flex-col',
        'w-[380px] h-[500px] max-h-[70vh]',
        'rounded-lg border border-border bg-card shadow-xl',
        'animate-in slide-in-from-bottom-4 fade-in-0 duration-200',
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border px-4 py-3">
        <h2 id="chat-title" className="font-semibold text-foreground">
          Todo Assistant
        </h2>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleNewConversation}
            className="text-xs"
          >
            New Chat
          </Button>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </Button>
        </div>
      </div>

      {/* Messages */}
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        className="flex-1"
      />

      {/* Error display */}
      {error && (
        <div className="px-4 py-2 bg-destructive/10 text-destructive text-sm">
          {error}
        </div>
      )}

      {/* Input */}
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="border-t border-border p-4"
      >
        <div className="flex gap-2">
          <Input
            ref={inputRef}
            type="text"
            placeholder="Type a message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            className="flex-1"
            aria-label="Chat message"
          />
          <Button
            type="submit"
            size="icon"
            disabled={!inputValue.trim() || isLoading}
            aria-label="Send message"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  );
}
