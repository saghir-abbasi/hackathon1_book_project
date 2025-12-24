import React, { useEffect, useCallback } from 'react';
import type { BackgroundModalProps } from './types';
import styles from './styles.module.css';

/**
 * BackgroundModal Component
 *
 * Modal dialog for selecting user's professional background.
 * Options: Software Developer or Hardware Engineer.
 */
export default function BackgroundModal({
  isOpen,
  onClose,
  onSelect,
}: BackgroundModalProps): JSX.Element | null {
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
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div
        className={styles.modal}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <h2 id="modal-title" className={styles.modalTitle}>
          Select Your Background
        </h2>
        <p className={styles.modalDescription}>
          Choose your professional background to personalize the content with relevant examples and analogies.
        </p>

        <div className={styles.modalOptions}>
          <button
            className={styles.optionButton}
            onClick={() => onSelect('software')}
            type="button"
          >
            <span className={styles.optionIcon}>💻</span>
            <span className={styles.optionLabel}>Software Developer</span>
            <span className={styles.optionDescription}>
              Code patterns, APIs, web development, databases
            </span>
          </button>

          <button
            className={styles.optionButton}
            onClick={() => onSelect('hardware')}
            type="button"
          >
            <span className={styles.optionIcon}>🔧</span>
            <span className={styles.optionLabel}>Hardware Engineer</span>
            <span className={styles.optionDescription}>
              Circuits, sensors, embedded systems, electronics
            </span>
          </button>
        </div>

        <button
          className={styles.modalCloseButton}
          onClick={onClose}
          type="button"
          aria-label="Close modal"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
