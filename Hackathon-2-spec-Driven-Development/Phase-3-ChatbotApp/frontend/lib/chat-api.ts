import type {
  ChatRequest,
  ChatResponse,
  ChatMessage,
  ConversationListResponse,
} from '@/types';
import { getToken, getUser, clearAuth } from './auth';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export class ChatApiError extends Error {
  constructor(
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'ChatApiError';
  }
}

/**
 * Chat API client for Phase III chatbot integration.
 * Handles all chat-related API calls with JWT authentication.
 */
class ChatApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = getToken();
    const user = getUser();

    if (!token || !user) {
      throw new ChatApiError('UNAUTHORIZED', 'Not authenticated');
    }

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...options.headers,
    };

    // Replace {user_id} placeholder in endpoint
    const resolvedEndpoint = endpoint.replace('{user_id}', user.id.toString());

    const response = await fetch(`${API_BASE}${resolvedEndpoint}`, {
      ...options,
      headers,
    });

    // Handle 401 - redirect to login
    if (response.status === 401) {
      clearAuth();
      if (typeof window !== 'undefined') {
        window.location.href = '/login?session=expired';
      }
      throw new ChatApiError('UNAUTHORIZED', 'Session expired');
    }

    const data = await response.json();

    if (!response.ok) {
      const error = data.error || {
        code: 'UNKNOWN_ERROR',
        message: 'An error occurred',
      };
      throw new ChatApiError(error.code, error.message);
    }

    return data as T;
  }

  /**
   * Send a chat message to the AI assistant.
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>('/{user_id}/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * List all conversations for the current user.
   */
  async listConversations(): Promise<ConversationListResponse> {
    return this.request<ConversationListResponse>('/{user_id}/conversations');
  }

  /**
   * Get messages for a specific conversation.
   */
  async getConversationMessages(conversationId: number): Promise<{
    conversation: { id: number; title: string | null };
    messages: ChatMessage[];
  }> {
    return this.request(`/{user_id}/conversations/${conversationId}`, {
      method: 'GET'
    });
  }
}

export const chatApi = new ChatApiClient();

/**
 * Generate a temporary ID for optimistic updates.
 */
export function generateMessageId(): string {
  return `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}
