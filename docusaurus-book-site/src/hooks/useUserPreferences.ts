import { useState, useEffect, useCallback } from 'react';

// Import auth context - wrapped in try/catch for SSR safety
let useAuthContext: () => { user: any; isAuthenticated: boolean; isLoading: boolean } | undefined;
try {
  const authModule = require('../auth/AuthContext');
  useAuthContext = authModule.useAuthContext;
} catch {
  useAuthContext = undefined;
}

/**
 * User's professional background for content personalization.
 */
export type UserBackground = 'software' | 'hardware' | null;

/**
 * User preferences stored in localStorage.
 */
export interface UserPreferences {
  background: UserBackground;
  lastUpdated: string;
}

const STORAGE_KEY = 'book_user_preferences';

/**
 * Default preferences when none are stored.
 */
const DEFAULT_PREFERENCES: UserPreferences = {
  background: null,
  lastUpdated: new Date().toISOString(),
};

/**
 * Custom hook for managing user preferences.
 *
 * Priority:
 * 1. If authenticated: use server-side user preference
 * 2. If not authenticated: fall back to localStorage
 *
 * Provides read/write access to user background preference for content personalization.
 */
export function useUserPreferences() {
  const [localPreferences, setLocalPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES);
  const [isLoaded, setIsLoaded] = useState(false);

  // Try to get auth context (may not be available during SSR)
  let authContext: { user: any; isAuthenticated: boolean; isLoading: boolean } | undefined;
  try {
    if (useAuthContext) {
      authContext = useAuthContext();
    }
  } catch {
    // Auth context not available (outside provider or SSR)
    authContext = undefined;
  }

  const isAuthenticated = authContext?.isAuthenticated ?? false;
  const authUser = authContext?.user;
  const authLoading = authContext?.isLoading ?? false;

  // Load preferences from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') return;

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as UserPreferences;
        // Validate the stored data
        if (
          parsed.background === 'software' ||
          parsed.background === 'hardware' ||
          parsed.background === null
        ) {
          setLocalPreferences(parsed);
        }
      }
    } catch (error) {
      console.warn('Failed to load user preferences:', error);
    } finally {
      setIsLoaded(true);
    }
  }, []);

  /**
   * Update user background preference in localStorage.
   * Note: For authenticated users, use the auth context's updatePreference instead.
   */
  const setBackground = useCallback((background: UserBackground) => {
    const newPreferences: UserPreferences = {
      background,
      lastUpdated: new Date().toISOString(),
    };

    setLocalPreferences(newPreferences);

    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newPreferences));
      } catch (error) {
        console.warn('Failed to save user preferences:', error);
      }
    }
  }, []);

  /**
   * Clear all user preferences from localStorage.
   */
  const clearPreferences = useCallback(() => {
    setLocalPreferences(DEFAULT_PREFERENCES);

    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (error) {
        console.warn('Failed to clear user preferences:', error);
      }
    }
  }, []);

  // Determine the effective background preference
  // Priority: authenticated user's server preference > localStorage
  const effectiveBackground: UserBackground = isAuthenticated && authUser?.background
    ? authUser.background
    : localPreferences.background;

  /**
   * Check if user has set their background preference.
   */
  const hasBackground = effectiveBackground !== null;

  /**
   * Get localStorage preference (useful for migration during signup).
   */
  const getLocalStoragePreference = useCallback((): UserBackground => {
    if (typeof window === 'undefined') return null;

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as UserPreferences;
        if (parsed.background === 'software' || parsed.background === 'hardware') {
          return parsed.background;
        }
      }
    } catch {
      // Ignore errors
    }
    return null;
  }, []);

  return {
    preferences: {
      background: effectiveBackground,
      lastUpdated: isAuthenticated && authUser
        ? authUser.created_at
        : localPreferences.lastUpdated,
    },
    background: effectiveBackground,
    hasBackground,
    isLoaded: isLoaded && !authLoading,
    isAuthenticated,
    user: authUser,
    setBackground,
    clearPreferences,
    getLocalStoragePreference,
  };
}

export default useUserPreferences;
