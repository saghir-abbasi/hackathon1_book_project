import React, { useState, useEffect, FormEvent } from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth, BackgroundType } from '../../auth';
import { useUserPreferences } from '../../hooks/useUserPreferences';
import styles from './Auth.module.css';

interface SignUpFormProps {
  onSuccess?: () => void;
  initialBackground?: BackgroundType | null;
}

const STORAGE_KEY = 'book_user_preferences';

/**
 * Signup form component with email, password, and background selection.
 * Supports migration from localStorage preferences.
 */
export function SignUpForm({ onSuccess, initialBackground }: SignUpFormProps) {
  const { signUp, isLoading, error, clearError } = useAuth();
  const { getLocalStoragePreference, clearPreferences } = useUserPreferences();
  const signInUrl = useBaseUrl('/auth/signin');

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [background, setBackground] = useState<BackgroundType | ''>(initialBackground || '');
  const [localError, setLocalError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [hasExistingPreference, setHasExistingPreference] = useState(false);

  // Check for existing localStorage preference on mount
  useEffect(() => {
    const existingPref = getLocalStoragePreference();
    if (existingPref && !background) {
      setBackground(existingPref);
      setHasExistingPreference(true);
    }
  }, [getLocalStoragePreference, background]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    // Validate form
    if (!email || !password || !background) {
      setLocalError('Please fill in all required fields');
      return;
    }

    if (password.length < 8) {
      setLocalError('Password must be at least 8 characters');
      return;
    }

    if (password !== confirmPassword) {
      setLocalError('Passwords do not match');
      return;
    }

    try {
      await signUp(email, password, background as BackgroundType);
      // Clear localStorage preference after successful signup (migration complete)
      clearPreferences();
      onSuccess?.();
    } catch (err) {
      // Error is handled by the auth context
    }
  };

  const displayError = localError || error;

  return (
    <form className={styles.authForm} onSubmit={handleSubmit}>
      <h2 className={styles.formTitle}>Create Account</h2>

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
            placeholder="At least 8 characters"
            required
            minLength={8}
            disabled={isLoading}
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

      <div className={styles.formGroup}>
        <label htmlFor="confirmPassword" className={styles.label}>
          Confirm Password
        </label>
        <input
          type={showPassword ? 'text' : 'password'}
          id="confirmPassword"
          className={styles.input}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Re-enter your password"
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.formGroup}>
        <label className={styles.label}>
          Your Background <span className={styles.required}>*</span>
        </label>
        {hasExistingPreference && (
          <p className={styles.helperText} style={{ color: 'var(--ifm-color-success)' }}>
            We found your existing preference. You can keep it or choose a different one.
          </p>
        )}
        <p className={styles.helperText}>
          This helps us personalize the content for your learning experience.
        </p>
        <div className={styles.radioGroup}>
          <label className={styles.radioLabel}>
            <input
              type="radio"
              name="background"
              value="software"
              checked={background === 'software'}
              onChange={() => setBackground('software')}
              disabled={isLoading}
              className={styles.radioInput}
            />
            <span className={styles.radioText}>
              <strong>Software Developer</strong>
              <span className={styles.radioDescription}>
                I have experience with programming and software development
              </span>
            </span>
          </label>
          <label className={styles.radioLabel}>
            <input
              type="radio"
              name="background"
              value="hardware"
              checked={background === 'hardware'}
              onChange={() => setBackground('hardware')}
              disabled={isLoading}
              className={styles.radioInput}
            />
            <span className={styles.radioText}>
              <strong>Hardware Engineer</strong>
              <span className={styles.radioDescription}>
                I have experience with electronics and hardware systems
              </span>
            </span>
          </label>
        </div>
      </div>

      <button
        type="submit"
        className={styles.submitButton}
        disabled={isLoading || !email || !password || !background}
      >
        {isLoading ? 'Creating Account...' : 'Create Account'}
      </button>

      <p className={styles.footerText}>
        Already have an account?{' '}
        <a href={signInUrl} className={styles.link}>
          Sign In
        </a>
      </p>
    </form>
  );
}

export default SignUpForm;
