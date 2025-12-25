import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../../auth';
import { UserMenu } from './UserMenu';
import styles from './Auth.module.css';

/**
 * Navbar authentication component.
 * Shows sign in/sign up links when not authenticated, or user menu when authenticated.
 */
export function NavbarAuth() {
  const { isAuthenticated, isLoading } = useAuth();
  const signInUrl = useBaseUrl('/auth/signin');
  const signUpUrl = useBaseUrl('/auth/signup');

  // Don't render anything while loading to prevent flash
  if (isLoading) {
    return null;
  }

  if (isAuthenticated) {
    return <UserMenu />;
  }

  return (
    <div className={styles.navbarAuthContainer}>
      <a href={signInUrl} className={styles.navbarSignIn}>
        Sign In
      </a>
      <a href={signUpUrl} className={styles.navbarSignUp}>
        Sign Up
      </a>
    </div>
  );
}

export default NavbarAuth;
