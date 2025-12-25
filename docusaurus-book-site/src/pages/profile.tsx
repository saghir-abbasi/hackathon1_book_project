import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../auth';
import { ProfileSettings } from '../components/Auth/ProfileSettings';

/**
 * Profile page component.
 */
export default function ProfilePage() {
  const { isAuthenticated, isLoading } = useAuth();
  const signInUrl = useBaseUrl('/auth/signin');

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      window.location.href = signInUrl;
    }
  }, [isAuthenticated, isLoading, signInUrl]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <Layout title="Profile">
        <main style={{ padding: '2rem 0', textAlign: 'center' }}>
          <p>Loading...</p>
        </main>
      </Layout>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!isAuthenticated) {
    return null;
  }

  return (
    <Layout
      title="Profile"
      description="Manage your profile settings and preferences"
    >
      <main style={{ padding: '2rem 0' }}>
        <ProfileSettings />
      </main>
    </Layout>
  );
}
