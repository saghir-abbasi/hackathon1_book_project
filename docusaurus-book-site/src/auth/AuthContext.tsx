import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

/**
 * User's professional background type.
 */
export type BackgroundType = 'software' | 'hardware';

/**
 * User data returned from the API.
 */
export interface User {
  id: string;
  email: string;
  background: BackgroundType;
  created_at: string;
}

/**
 * Auth context state.
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Auth context value with state and actions.
 */
export interface AuthContextValue extends AuthState {
  signUp: (email: string, password: string, background: BackgroundType) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  updatePreference: (background: BackgroundType) => Promise<void>;
  clearError: () => void;
  checkSession: () => Promise<void>;
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
 * Auth context.
 */
export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/**
 * Hook to access auth context.
 * @throws Error if used outside AuthProvider
 */
export function useAuthContext(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
