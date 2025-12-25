import { useAuthContext, BackgroundType, User, AuthContextValue } from './AuthContext';

/**
 * API base URL for authentication endpoints.
 */
const getApiBaseUrl = (): string => {
  if (typeof window === 'undefined') {
    return 'http://localhost:8000';
  }

  const hostname = window.location.hostname;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }

  // Production URL - adjust as needed
  return 'https://book-project-backend.vercel.app';
};

/**
 * API response types.
 */
interface AuthResponse {
  user: User;
  message: string;
}

interface SessionResponse {
  authenticated: boolean;
  user: User | null;
}

interface PreferenceResponse {
  background: BackgroundType;
}

interface ErrorResponse {
  error: {
    code: string;
    message: string;
  };
}

/**
 * Auth API client.
 */
export const authApi = {
  /**
   * Sign up a new user.
   */
  async signUp(email: string, password: string, background: BackgroundType): Promise<AuthResponse> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password, background }),
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.error?.message || 'Sign up failed');
    }

    return response.json();
  },

  /**
   * Sign in an existing user.
   */
  async signIn(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.error?.message || 'Sign in failed');
    }

    return response.json();
  },

  /**
   * Sign out the current user.
   */
  async signOut(): Promise<void> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/signout`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.error?.message || 'Sign out failed');
    }
  },

  /**
   * Get current session.
   */
  async getSession(): Promise<SessionResponse> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/session`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      // Session check failures are not errors, just unauthenticated
      return { authenticated: false, user: null };
    }

    return response.json();
  },

  /**
   * Update user preference.
   */
  async updatePreference(background: BackgroundType): Promise<PreferenceResponse> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/user/preference`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ background }),
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.error?.message || 'Update preference failed');
    }

    return response.json();
  },

  /**
   * Get user preference.
   */
  async getPreference(): Promise<PreferenceResponse> {
    const response = await fetch(`${getApiBaseUrl()}/api/auth/user/preference`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      const error: ErrorResponse = await response.json();
      throw new Error(error.error?.message || 'Get preference failed');
    }

    return response.json();
  },
};

/**
 * Hook to access authentication functionality.
 *
 * @example
 * ```tsx
 * const { user, isAuthenticated, signIn, signOut } = useAuth();
 *
 * if (isAuthenticated) {
 *   return <div>Welcome, {user.email}!</div>;
 * }
 * ```
 */
export function useAuth(): AuthContextValue {
  return useAuthContext();
}

export default useAuth;
