import React, { useState } from 'react';
import { useAuth } from '../../auth';
import styles from './Auth.module.css';

interface ProtectedLinkProps {
  to: string;
  className?: string;
  children: React.ReactNode;
}

/**
 * A link component that requires authentication.
 * If the user is not authenticated, shows a modal to sign in or sign up.
 */
export function ProtectedLink({ to, className, children }: ProtectedLinkProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    if (isLoading) {
      e.preventDefault();
      return;
    }

    if (!isAuthenticated) {
      e.preventDefault();
      setShowAuthModal(true);
    }
    // If authenticated, the link will work normally
  };

  const handleCloseModal = () => {
    setShowAuthModal(false);
  };

  const handleAuthSuccess = () => {
    setShowAuthModal(false);
    // Navigate to the protected page
    window.location.href = to;
  };

  return (
    <>
      <a href={to} className={className} onClick={handleClick}>
        {children}
      </a>

      {showAuthModal && (
        <AuthModal onClose={handleCloseModal} onSuccess={handleAuthSuccess} />
      )}
    </>
  );
}

interface AuthModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

/**
 * Modal component for sign in / sign up flow.
 */
function AuthModal({ onClose, onSuccess }: AuthModalProps) {
  const [mode, setMode] = useState<'signin' | 'signup'>('signin');

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <button className={styles.modalClose} onClick={onClose}>
          &times;
        </button>

        <div className={styles.modalHeader}>
          <h2>{mode === 'signin' ? 'Sign In to Continue' : 'Create Account'}</h2>
          <p className={styles.modalSubtitle}>
            {mode === 'signin'
              ? 'Sign in to access the book content'
              : 'Create an account to personalize your learning experience'}
          </p>
        </div>

        {mode === 'signin' ? (
          <SignInFormInline onSuccess={onSuccess} onSwitchMode={() => setMode('signup')} />
        ) : (
          <SignUpFormInline onSuccess={onSuccess} onSwitchMode={() => setMode('signin')} />
        )}
      </div>
    </div>
  );
}

interface InlineFormProps {
  onSuccess: () => void;
  onSwitchMode: () => void;
}

/**
 * Inline sign in form for modal.
 */
function SignInFormInline({ onSuccess, onSwitchMode }: InlineFormProps) {
  const { signIn, isLoading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    if (!email || !password) {
      setLocalError('Please enter your email and password');
      return;
    }

    try {
      await signIn(email, password);
      onSuccess();
    } catch (err) {
      // Error handled by auth context
    }
  };

  const displayError = localError || error;

  return (
    <form className={styles.inlineForm} onSubmit={handleSubmit}>
      {displayError && <div className={styles.errorMessage}>{displayError}</div>}

      <div className={styles.formGroup}>
        <label htmlFor="signin-email" className={styles.label}>Email</label>
        <input
          type="email"
          id="signin-email"
          className={styles.input}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signin-password" className={styles.label}>Password</label>
        <input
          type="password"
          id="signin-password"
          className={styles.input}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
          disabled={isLoading}
        />
      </div>

      <button type="submit" className={styles.submitButton} disabled={isLoading}>
        {isLoading ? 'Signing In...' : 'Sign In'}
      </button>

      <p className={styles.footerText}>
        Don't have an account?{' '}
        <button type="button" className={styles.linkButton} onClick={onSwitchMode}>
          Sign Up
        </button>
      </p>
    </form>
  );
}

/**
 * Inline sign up form for modal.
 */
function SignUpFormInline({ onSuccess, onSwitchMode }: InlineFormProps) {
  const { signUp, isLoading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [background, setBackground] = useState<'software' | 'hardware' | ''>('');
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    clearError();

    if (!email || !password || !background) {
      setLocalError('Please fill in all fields');
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
      await signUp(email, password, background);
      onSuccess();
    } catch (err) {
      // Error handled by auth context
    }
  };

  const displayError = localError || error;

  return (
    <form className={styles.inlineForm} onSubmit={handleSubmit}>
      {displayError && <div className={styles.errorMessage}>{displayError}</div>}

      <div className={styles.formGroup}>
        <label htmlFor="signup-email" className={styles.label}>Email</label>
        <input
          type="email"
          id="signup-email"
          className={styles.input}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signup-password" className={styles.label}>Password</label>
        <input
          type="password"
          id="signup-password"
          className={styles.input}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="At least 8 characters"
          required
          minLength={8}
          disabled={isLoading}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signup-confirm" className={styles.label}>Confirm Password</label>
        <input
          type="password"
          id="signup-confirm"
          className={styles.input}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Re-enter password"
          required
          disabled={isLoading}
        />
      </div>

      <div className={styles.formGroup}>
        <label className={styles.label}>Your Background</label>
        <div className={styles.radioGroupCompact}>
          <label className={styles.radioLabelCompact}>
            <input
              type="radio"
              name="background"
              value="software"
              checked={background === 'software'}
              onChange={() => setBackground('software')}
              disabled={isLoading}
            />
            <span>Software Developer</span>
          </label>
          <label className={styles.radioLabelCompact}>
            <input
              type="radio"
              name="background"
              value="hardware"
              checked={background === 'hardware'}
              onChange={() => setBackground('hardware')}
              disabled={isLoading}
            />
            <span>Hardware Engineer</span>
          </label>
        </div>
      </div>

      <button type="submit" className={styles.submitButton} disabled={isLoading || !background}>
        {isLoading ? 'Creating Account...' : 'Create Account'}
      </button>

      <p className={styles.footerText}>
        Already have an account?{' '}
        <button type="button" className={styles.linkButton} onClick={onSwitchMode}>
          Sign In
        </button>
      </p>
    </form>
  );
}

export default ProtectedLink;
