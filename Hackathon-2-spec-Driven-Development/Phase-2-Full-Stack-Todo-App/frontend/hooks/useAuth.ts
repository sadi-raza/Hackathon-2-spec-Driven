'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { api, ApiError } from '@/lib/api';
import {
  getToken,
  getUser,
  saveAuthResponse,
  clearAuth,
  isAuthenticated as checkIsAuthenticated,
} from '@/lib/auth';
import type { AuthState } from '@/types';

export function useAuth() {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Initialize auth state from localStorage
  useEffect(() => {
    const token = getToken();
    const user = getUser();

    setState({
      user,
      isAuthenticated: !!token && !!user,
      isLoading: false,
    });
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        const response = await api.auth.login(email, password);
        saveAuthResponse(response.token, response.user);

        setState({
          user: response.user,
          isAuthenticated: true,
          isLoading: false,
        });

        toast.success('Welcome back!');
        router.push('/dashboard');
      } catch (error) {
        if (error instanceof ApiError) {
          toast.error(error.message);
        } else {
          toast.error('An unexpected error occurred');
        }
        throw error;
      }
    },
    [router]
  );

  const signup = useCallback(
    async (email: string, password: string) => {
      try {
        const response = await api.auth.signup(email, password);
        saveAuthResponse(response.token, response.user);

        setState({
          user: response.user,
          isAuthenticated: true,
          isLoading: false,
        });

        toast.success('Account created successfully!');
        router.push('/dashboard');
      } catch (error) {
        if (error instanceof ApiError) {
          toast.error(error.message);
        } else {
          toast.error('An unexpected error occurred');
        }
        throw error;
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    try {
      await api.auth.logout();
    } catch {
      // Ignore logout API errors, clear local state anyway
    }

    clearAuth();
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });

    toast.success('Logged out successfully');
    router.push('/login');
  }, [router]);

  return {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    login,
    signup,
    logout,
  };
}

// Hook for protecting routes
export function useRequireAuth() {
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    if (!checkIsAuthenticated()) {
      router.replace('/login');
    } else {
      setIsChecking(false);
    }
  }, [router]);

  return { isChecking };
}
