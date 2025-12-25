import React, { useState, useRef, useEffect } from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../../auth';
import styles from './Auth.module.css';

/**
 * User menu component showing user email and dropdown with options.
 */
export function UserMenu() {
  const { user, signOut, isLoading } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const homeUrl = useBaseUrl('/');
  const profileUrl = useBaseUrl('/profile');

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSignOut = async () => {
    setIsOpen(false);
    await signOut();
    window.location.href = homeUrl;
  };

  if (!user) {
    return null;
  }

  return (
    <div className={styles.userMenu} ref={menuRef}>
      <button
        className={styles.userButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <span className={styles.userEmail}>{user.email}</span>
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          style={{ transform: isOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}
        >
          <path
            d="M2.5 4.5L6 8L9.5 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isOpen && (
        <div className={styles.dropdown}>
          <div className={styles.dropdownLabel}>
            Background: {user.background}
          </div>
          <div className={styles.dropdownDivider} />
          <a href={profileUrl} className={styles.dropdownItem}>
            Profile Settings
          </a>
          <div className={styles.dropdownDivider} />
          <button
            className={styles.dropdownItem}
            onClick={handleSignOut}
            disabled={isLoading}
          >
            {isLoading ? 'Signing out...' : 'Sign Out'}
          </button>
        </div>
      )}
    </div>
  );
}

export default UserMenu;
