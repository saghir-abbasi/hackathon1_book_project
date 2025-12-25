import React, { useState, useCallback, useEffect, ReactNode } from 'react';
import { AuthContext, AuthState, User, BackgroundType } from './AuthContext';
import { authApi } from './useAuth';

/**
 * Props for AuthProvider.
 */
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Default auth state.
 */
const DEFAULT_AUTH_STATE: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

/**
 * Auth provider component that wraps the app and provides authentication state.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>(DEFAULT_AUTH_STATE);

  /**
   * Check current session on mount.
   */
  const checkSession = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const response = await authApi.getSession();

      setState({
        user: response.user,
        isAuthenticated: response.authenticated,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      // Session check failed - user is not authenticated
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null, // Don't show error for session check failures
      });
    }
  }, []);

  /**
   * Sign up a new user.
   */
  const signUp = useCallback(async (email: string, password: string, background: BackgroundType) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const response = await authApi.signUp(email, password, background);

      setState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Sign up failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Sign in an existing user.
   */
  const signIn = useCallback(async (email: string, password: string) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const response = await authApi.signIn(email, password);

      setState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Sign in failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Sign out the current user.
   */
  const signOut = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      await authApi.signOut();

      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      // Even if signout fails on server, clear local state
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  }, []);

  /**
   * Update user preference.
   */
  const updatePreference = useCallback(async (background: BackgroundType) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      await authApi.updatePreference(background);

      // Update user in state with new background
      setState(prev => ({
        ...prev,
        user: prev.user ? { ...prev.user, background } : null,
        isLoading: false,
        error: null,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Update preference failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Clear error state.
   */
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Check session on mount
  useEffect(() => {
    checkSession();
  }, [checkSession]);

  const value = {
    ...state,
    signUp,
    signIn,
    signOut,
    updatePreference,
    clearError,
    checkSession,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
