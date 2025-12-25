import React, { useState } from 'react';
import { useAuth, BackgroundType } from '../../auth';
import styles from './Auth.module.css';

/**
 * Profile settings component for viewing and updating user preferences.
 */
export function ProfileSettings() {
  const { user, updatePreference, isLoading, error, clearError } = useAuth();
  const [selectedBackground, setSelectedBackground] = useState<BackgroundType | null>(
    user?.background || null
  );
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  if (!user) {
    return (
      <div className={styles.profileContainer}>
        <div className={styles.errorMessage}>
          Please sign in to view your profile.
        </div>
      </div>
    );
  }

  const handleSave = async () => {
    if (!selectedBackground || selectedBackground === user.background) {
      return;
    }

    clearError();
    setSuccessMessage(null);

    try {
      await updatePreference(selectedBackground);
      setSuccessMessage('Preference updated successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      // Error handled by auth context
    }
  };

  const hasChanges = selectedBackground !== user.background;

  return (
    <div className={styles.profileContainer}>
      <div className={styles.profileCard}>
        <div className={styles.profileHeader}>
          <h1 className={styles.profileTitle}>Profile Settings</h1>
        </div>

        {error && (
          <div className={styles.errorMessage}>
            {error}
          </div>
        )}

        {successMessage && (
          <div className={styles.successMessage}>
            {successMessage}
          </div>
        )}

        <div className={styles.profileSection}>
          <span className={styles.profileLabel}>Email</span>
          <span className={styles.profileValue}>{user.email}</span>
        </div>

        <div className={styles.profileSection}>
          <span className={styles.profileLabel}>Member Since</span>
          <span className={styles.profileValue}>
            {new Date(user.created_at).toLocaleDateString()}
          </span>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Your Background
          </label>
          <p className={styles.helperText}>
            This affects how content is personalized for your learning experience.
          </p>
          <div className={styles.radioGroup}>
            <label className={styles.radioLabel}>
              <input
                type="radio"
                name="background"
                value="software"
                checked={selectedBackground === 'software'}
                onChange={() => setSelectedBackground('software')}
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
                checked={selectedBackground === 'hardware'}
                onChange={() => setSelectedBackground('hardware')}
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
          className={styles.submitButton}
          onClick={handleSave}
          disabled={isLoading || !hasChanges}
        >
          {isLoading ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
}

export default ProfileSettings;
