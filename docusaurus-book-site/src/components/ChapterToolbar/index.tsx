import React, { useState, useCallback, useEffect, useRef } from 'react';
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
 * Get the content container element
 */
function getContentContainer(): HTMLElement | null {
  const selectors = [
    '.theme-doc-markdown',
    '[class*="docItemContent"]',
    'article .markdown',
    'article',
  ];

  for (const selector of selectors) {
    const element = document.querySelector(selector) as HTMLElement;
    if (element) {
      return element;
    }
  }
  return null;
}

interface ChapterToolbarProps {
  /** When true, renders compact buttons without container (for navbar) */
  compact?: boolean;
}

/**
 * ChapterToolbar Component
 *
 * Renders a toolbar at the top of each documentation chapter with:
 * - Personalize button: Adapts content to user's background (Software/Hardware)
 * - Translate button: Translates content to Urdu (displayed inline)
 *
 * Manages the transformation state and content display.
 */
export default function ChapterToolbar({ compact = false }: ChapterToolbarProps): JSX.Element {
  const [transformState, setTransformState] = useState<TransformationState>(
    INITIAL_TRANSFORMATION_STATE
  );
  const contentContainerRef = useRef<HTMLElement | null>(null);
  const translatedContentRef = useRef<HTMLDivElement | null>(null);

  /**
   * Called when a transformation starts.
   */
  const handleTransformStart = useCallback((type: TransformationType) => {
    const isTranslate = type === 'translate';

    // Store original content for both translation and personalization
    let originalContent: string | null = null;
    const container = getContentContainer();
    if (container) {
      originalContent = container.innerHTML;
      contentContainerRef.current = container;
    }

    setTransformState({
      status: 'loading',
      type,
      content: '',
      error: null,
      showOverlay: false, // Always use inline display
      isRtl: isTranslate,
      showInline: true, // Both translation and personalization are inline
      originalContent,
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
   * Restore original content (for translation).
   */
  const handleShowOriginal = useCallback(() => {
    if (contentContainerRef.current && transformState.originalContent) {
      contentContainerRef.current.innerHTML = transformState.originalContent;
      contentContainerRef.current.removeAttribute('dir');
      contentContainerRef.current.style.fontFamily = '';
      contentContainerRef.current.style.lineHeight = '';
    }
    setTransformState(INITIAL_TRANSFORMATION_STATE);
  }, [transformState.originalContent]);

  /**
   * Retry the last transformation.
   */
  const handleRetry = useCallback(() => {
    setTransformState((prev) => ({
      ...prev,
      status: 'idle',
      content: '',
      error: null,
    }));
  }, []);

  /**
   * Update inline content when transformation streams in.
   */
  useEffect(() => {
    if (transformState.showInline && contentContainerRef.current) {
      const container = contentContainerRef.current;
      const isTranslation = transformState.type === 'translate';

      if (transformState.status === 'loading' && !transformState.content) {
        // Show loading state
        if (isTranslation) {
          container.innerHTML = `
            <div class="${styles.inlineLoading}">
              <div class="${styles.spinner}"></div>
              <p>اردو میں ترجمہ ہو رہا ہے...</p>
              <p style="font-size: 0.9rem; opacity: 0.7;">Translating to Urdu...</p>
            </div>
          `;
          container.setAttribute('dir', 'rtl');
          container.style.fontFamily = "'Noto Nastaliq Urdu', serif";
        } else {
          container.innerHTML = `
            <div class="${styles.inlineLoading}">
              <div class="${styles.spinner}"></div>
              <p>Personalizing content for your background...</p>
              <p style="font-size: 0.9rem; opacity: 0.7;">This may take a moment</p>
            </div>
          `;
          container.removeAttribute('dir');
          container.style.fontFamily = '';
        }
      } else if (transformState.content) {
        // Convert plain text with line breaks to proper HTML paragraphs
        const formattedContent = transformState.content
          .split(/\n\n+/)
          .map(para => para.trim())
          .filter(para => para.length > 0)
          .map(para => {
            // Check if it's a heading (starts with #)
            if (para.startsWith('# ')) {
              return `<h1>${para.substring(2)}</h1>`;
            } else if (para.startsWith('## ')) {
              return `<h2>${para.substring(3)}</h2>`;
            } else if (para.startsWith('### ')) {
              return `<h3>${para.substring(4)}</h3>`;
            } else if (para.startsWith('#### ')) {
              return `<h4>${para.substring(5)}</h4>`;
            } else if (para.startsWith('- ') || para.startsWith('* ')) {
              // Handle list items
              const items = para.split(/\n/).map(item =>
                `<li>${item.replace(/^[-*]\s*/, '')}</li>`
              ).join('');
              return `<ul>${items}</ul>`;
            } else if (/^\d+\.\s/.test(para)) {
              // Handle numbered lists
              const items = para.split(/\n/).map(item =>
                `<li>${item.replace(/^\d+\.\s*/, '')}</li>`
              ).join('');
              return `<ol>${items}</ol>`;
            } else if (para.startsWith('```')) {
              // Handle code blocks
              const code = para.replace(/^```\w*\n?/, '').replace(/```$/, '');
              return `<pre><code>${code}</code></pre>`;
            } else {
              return `<p>${para.replace(/\n/g, '<br/>')}</p>`;
            }
          })
          .join('\n');

        if (isTranslation) {
          container.innerHTML = `
            <div class="${styles.translatedContent}" dir="rtl">
              ${formattedContent}
              ${transformState.status === 'streaming' ? `<span class="${styles.cursor}">▋</span>` : ''}
            </div>
          `;
          container.setAttribute('dir', 'rtl');
          container.style.fontFamily = "'Noto Nastaliq Urdu', serif";
          container.style.lineHeight = '2.2';
        } else {
          container.innerHTML = `
            <div class="${styles.personalizedContent}">
              ${formattedContent}
              ${transformState.status === 'streaming' ? `<span class="${styles.cursor}">▋</span>` : ''}
            </div>
          `;
          container.removeAttribute('dir');
          container.style.fontFamily = '';
          container.style.lineHeight = '';
        }
      }

      if (transformState.status === 'error') {
        const errorType = isTranslation ? 'Translation' : 'Personalization';
        container.innerHTML = `
          <div class="${styles.inlineError}">
            <p>⚠️ ${transformState.error || `${errorType} failed`}</p>
            <button onclick="window.location.reload()">Refresh Page</button>
          </div>
        `;
      }
    }
  }, [transformState]);

  const isProcessing = transformState.status === 'loading' || transformState.status === 'streaming';
  const showRestoreButton = transformState.showInline && (transformState.status === 'streaming' || transformState.status === 'complete');

  const buttons = (
    <>
      <PersonalizeButton
        onTransformStart={handleTransformStart}
        onContentChunk={handleContentChunk}
        onTransformComplete={handleTransformComplete}
        onTransformError={handleTransformError}
        disabled={isProcessing}
        compact={compact}
      />
      {showRestoreButton ? (
        <button
          className={compact ? styles.navbarButton : `${styles.toolbarButton} ${styles.restoreButton}`}
          onClick={handleShowOriginal}
          type="button"
        >
          <span className={compact ? styles.navbarButtonIcon : styles.buttonIcon}>↩️</span>
          <span className={compact ? styles.navbarButtonText : styles.buttonText}>Show Original</span>
        </button>
      ) : (
        <TranslateButton
          onTransformStart={handleTransformStart}
          onContentChunk={handleContentChunk}
          onTransformComplete={handleTransformComplete}
          onTransformError={handleTransformError}
          disabled={isProcessing}
          compact={compact}
        />
      )}
    </>
  );

  // Compact mode: render buttons directly without container (for navbar)
  if (compact) {
    return (
      <>
        <div className={styles.navbarToolbar}>
          {buttons}
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

  // Full mode: render with container styling
  return (
    <>
      <div className={styles.toolbar}>
        <div className={styles.toolbarContent}>
          {buttons}
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
