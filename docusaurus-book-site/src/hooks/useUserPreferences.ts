import { useState, useEffect, useCallback } from 'react';

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
 * Custom hook for managing user preferences in localStorage.
 * Provides read/write access to user background preference for content personalization.
 */
export function useUserPreferences() {
  const [preferences, setPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES);
  const [isLoaded, setIsLoaded] = useState(false);

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
          setPreferences(parsed);
        }
      }
    } catch (error) {
      console.warn('Failed to load user preferences:', error);
    } finally {
      setIsLoaded(true);
    }
  }, []);

  /**
   * Update user background preference.
   */
  const setBackground = useCallback((background: UserBackground) => {
    const newPreferences: UserPreferences = {
      background,
      lastUpdated: new Date().toISOString(),
    };

    setPreferences(newPreferences);

    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newPreferences));
      } catch (error) {
        console.warn('Failed to save user preferences:', error);
      }
    }
  }, []);

  /**
   * Clear all user preferences.
   */
  const clearPreferences = useCallback(() => {
    setPreferences(DEFAULT_PREFERENCES);

    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (error) {
        console.warn('Failed to clear user preferences:', error);
      }
    }
  }, []);

  /**
   * Check if user has set their background preference.
   */
  const hasBackground = preferences.background !== null;

  return {
    preferences,
    background: preferences.background,
    hasBackground,
    isLoaded,
    setBackground,
    clearPreferences,
  };
}

export default useUserPreferences;
