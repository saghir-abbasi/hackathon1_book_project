import React, { useEffect, useCallback } from 'react';
import type { ContentOverlayProps } from './types';
import styles from './styles.module.css';

/**
 * ContentOverlay Component
 *
 * Displays the transformed content (personalized or translated) in an overlay.
 * Supports streaming content display with loading states and RTL for Urdu.
 */
export default function ContentOverlay({
  state,
  onClose,
  onRetry,
}: ContentOverlayProps): JSX.Element {
  const { status, type, content, error, isRtl } = state;

  /**
   * Handle keyboard events for accessibility.
   */
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    },
    [onClose]
  );

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [handleKeyDown]);

  /**
   * Get the title based on transformation type.
   */
  const getTitle = () => {
    if (type === 'personalize') {
      return 'Personalized Content';
    }
    if (type === 'translate') {
      return 'اردو ترجمہ'; // Urdu Translation
    }
    return 'Transformed Content';
  };

  /**
   * Render loading spinner.
   */
  const renderLoading = () => (
    <div className={styles.loadingContainer}>
      <div className={styles.spinner}></div>
      <p className={styles.loadingText}>
        {type === 'translate' ? 'Translating to Urdu...' : 'Personalizing content...'}
      </p>
    </div>
  );

  /**
   * Render error state.
   */
  const renderError = () => (
    <div className={styles.errorContainer}>
      <span className={styles.errorIcon}>⚠️</span>
      <p className={styles.errorText}>{error || 'An error occurred'}</p>
      {onRetry && (
        <button className={styles.retryButton} onClick={onRetry} type="button">
          Try Again
        </button>
      )}
    </div>
  );

  /**
   * Render content.
   */
  const renderContent = () => (
    <div
      className={`${styles.contentBody} ${isRtl ? styles.rtlContent : ''}`}
      dir={isRtl ? 'rtl' : 'ltr'}
    >
      {content || (status === 'loading' ? '' : 'No content generated.')}
      {status === 'streaming' && <span className={styles.cursor}>▋</span>}
    </div>
  );

  return (
    <div className={styles.overlay}>
      <div className={styles.overlayHeader}>
        <h2 className={`${styles.overlayTitle} ${isRtl ? styles.rtlText : ''}`}>
          {getTitle()}
        </h2>
        <button
          className={styles.closeButton}
          onClick={onClose}
          type="button"
          aria-label="Close overlay"
        >
          ✕
        </button>
      </div>

      <div className={styles.overlayContent}>
        {status === 'loading' && !content && renderLoading()}
        {status === 'error' && renderError()}
        {(status === 'streaming' || status === 'complete' || content) && renderContent()}
      </div>

      <div className={styles.overlayFooter}>
        <button className={styles.closeFooterButton} onClick={onClose} type="button">
          Close
        </button>
        {status === 'complete' && (
          <span className={styles.completeIndicator}>✓ Complete</span>
        )}
      </div>
    </div>
  );
}
