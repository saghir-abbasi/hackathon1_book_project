import React, { useState, useCallback } from 'react';
import {
  TransformationState,
  TransformationType,
  INITIAL_TRANSFORMATION_STATE,
} from './types';
import PersonalizeButton from './PersonalizeButton';
import TranslateButton from './TranslateButton';
import ContentOverlay from './ContentOverlay';
import styles from './styles.module.css';

/**
 * ChapterToolbar Component
 *
 * Renders a toolbar at the top of each documentation chapter with:
 * - Personalize button: Adapts content to user's background (Software/Hardware)
 * - Translate button: Translates content to Urdu
 *
 * Manages the transformation state and content overlay display.
 */
export default function ChapterToolbar(): JSX.Element {
  const [transformState, setTransformState] = useState<TransformationState>(
    INITIAL_TRANSFORMATION_STATE
  );

  /**
   * Called when a transformation starts.
   */
  const handleTransformStart = useCallback((type: TransformationType) => {
    setTransformState({
      status: 'loading',
      type,
      content: '',
      error: null,
      showOverlay: true,
      isRtl: type === 'translate',
    });
  }, []);

  /**
   * Called when a content chunk is received from streaming.
   */
  const handleContentChunk = useCallback((chunk: string) => {
    setTransformState((prev) => ({
      ...prev,
      status: 'streaming',
      content: prev.content + chunk,
    }));
  }, []);

  /**
   * Called when transformation completes successfully.
   */
  const handleTransformComplete = useCallback(() => {
    setTransformState((prev) => ({
      ...prev,
      status: 'complete',
    }));
  }, []);

  /**
   * Called when transformation encounters an error.
   */
  const handleTransformError = useCallback((error: string) => {
    setTransformState((prev) => ({
      ...prev,
      status: 'error',
      error,
    }));
  }, []);

  /**
   * Close the content overlay and reset state.
   */
  const handleCloseOverlay = useCallback(() => {
    setTransformState(INITIAL_TRANSFORMATION_STATE);
  }, []);

  /**
   * Retry the last transformation.
   */
  const handleRetry = useCallback(() => {
    // Reset to allow retrying - the button will handle the actual retry
    setTransformState((prev) => ({
      ...prev,
      status: 'idle',
      content: '',
      error: null,
    }));
  }, []);

  const isProcessing = transformState.status === 'loading' || transformState.status === 'streaming';

  return (
    <>
      <div className={styles.toolbar}>
        <div className={styles.toolbarContent}>
          <PersonalizeButton
            onTransformStart={handleTransformStart}
            onContentChunk={handleContentChunk}
            onTransformComplete={handleTransformComplete}
            onTransformError={handleTransformError}
            disabled={isProcessing}
          />
          <TranslateButton
            onTransformStart={handleTransformStart}
            onContentChunk={handleContentChunk}
            onTransformComplete={handleTransformComplete}
            onTransformError={handleTransformError}
            disabled={isProcessing}
          />
        </div>
      </div>

      {transformState.showOverlay && (
        <ContentOverlay
          state={transformState}
          onClose={handleCloseOverlay}
          onRetry={handleRetry}
        />
      )}
    </>
  );
}
