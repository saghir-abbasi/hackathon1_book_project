import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../../auth';
import { SignUpForm } from '../../components/Auth/SignUpForm';

/**
 * Signup page component.
 */
export default function SignupPage() {
  const { isAuthenticated, user } = useAuth();

  // Redirect to home if already authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      window.location.href = '/';
    }
  }, [isAuthenticated, user]);

  const handleSuccess = () => {
    // Show success message briefly, then redirect
    setTimeout(() => {
      window.location.href = '/';
    }, 1500);
  };

  return (
    <Layout
      title="Sign Up"
      description="Create an account to personalize your learning experience"
    >
      <main style={{ padding: '2rem 0' }}>
        <div className="container">
          <SignUpForm onSuccess={handleSuccess} />
        </div>
      </main>
    </Layout>
  );
}
