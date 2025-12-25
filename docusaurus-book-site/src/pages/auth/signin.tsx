import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../../auth';
import { SignInForm } from '../../components/Auth/SignInForm';

/**
 * Sign in page component.
 */
export default function SigninPage() {
  const { isAuthenticated, user } = useAuth();

  // Redirect to home if already authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      window.location.href = '/';
    }
  }, [isAuthenticated, user]);

  const handleSuccess = () => {
    // Redirect after successful sign in
    window.location.href = '/';
  };

  return (
    <Layout
      title="Sign In"
      description="Sign in to access your personalized learning experience"
    >
      <main style={{ padding: '2rem 0' }}>
        <div className="container">
          <SignInForm onSuccess={handleSuccess} />
        </div>
      </main>
    </Layout>
  );
}
