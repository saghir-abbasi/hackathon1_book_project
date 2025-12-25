import React, { useState, FormEvent } from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../../auth';
import styles from './Auth.module.css';

interface SignInFormProps {
  onSuccess?: () => void;
}

/**
 * Sign in form component with email and password.
 */
export function SignInForm({ onSuccess }: SignInFormProps) {
  const { signIn, isLoading, error, clearError } = useAuth();
  const signUpUrl = useBaseUrl('/auth/signup');

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    // Validate form
    if (!email || !password) {
      setLocalError('Please enter your email and password');
      return;
    }

    try {
      await signIn(email, password);
      onSuccess?.();
    } catch (err) {
      // Error is handled by the auth context
    }
  };

  const displayError = localError || error;

  return (
    <form className={styles.authForm} onSubmit={handleSubmit}>
      <h2 className={styles.formTitle}>Sign In</h2>

      {displayError && (
        <div className={styles.errorMessage}>
          {displayError}
        </div>
      )}

      <div className={styles.formGroup}>
        <label htmlFor="email" className={styles.label}>
          Email Address
        </label>
        <input
          type="email"
          id="email"
          className={styles.input}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
          disabled={isLoading}
          autoComplete="email"
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="password" className={styles.label}>
          Password
        </label>
        <div className={styles.passwordWrapper}>
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            className={styles.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            disabled={isLoading}
            autoComplete="current-password"
          />
          <button
            type="button"
            className={styles.passwordToggle}
            onClick={() => setShowPassword(!showPassword)}
            tabIndex={-1}
          >
            {showPassword ? 'Hide' : 'Show'}
          </button>
        </div>
      </div>

      <button
        type="submit"
        className={styles.submitButton}
        disabled={isLoading || !email || !password}
      >
        {isLoading ? 'Signing In...' : 'Sign In'}
      </button>

      <p className={styles.footerText}>
        Don't have an account?{' '}
        <a href={signUpUrl} className={styles.link}>
          Sign Up
        </a>
      </p>
    </form>
  );
}

export default SignInForm;
