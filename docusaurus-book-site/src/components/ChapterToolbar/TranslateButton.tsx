import React, { useCallback, useRef } from 'react';
import type { TranslateButtonProps } from './types';
import AgentBridge from '@site/src/agent-client/agentBridge';
import styles from './styles.module.css';

/**
 * Prompt template for Urdu translation.
 */
const TRANSLATE_URDU_PROMPT = `
Translate the following robotics educational content to Urdu.

INSTRUCTIONS:
1. Translate all explanatory text to Urdu
2. Keep technical terms in English where no standard Urdu equivalent exists (e.g., "ROS 2", "node", "topic", "publisher", "subscriber")
3. For code blocks, keep the code in English but translate comments to Urdu
4. Maintain the same Markdown structure
5. Ensure the translation is clear, educational, and readable
6. Use formal Urdu appropriate for technical education

ORIGINAL CONTENT:
`;

/**
 * Extract chapter content from the page.
 */
function extractChapterContent(): string {
  const contentElement = document.querySelector('.theme-doc-markdown');
  if (!contentElement) {
    throw new Error('Could not find chapter content');
  }
  return contentElement.textContent || '';
}

/**
 * Get chapter ID from the current URL.
 */
function getChapterId(): string {
  const path = window.location.pathname;
  const segments = path.split('/').filter(Boolean);
  return segments[segments.length - 1] || 'unknown-chapter';
}

/**
 * Generate a unique session ID.
 */
function generateSessionId(): string {
  return `translate-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * TranslateButton Component
 *
 * Button that triggers content translation to Urdu.
 * Uses the Agent API to stream the translated content.
 */
export default function TranslateButton({
  onTransformStart,
  onContentChunk,
  onTransformComplete,
  onTransformError,
  disabled = false,
}: TranslateButtonProps): JSX.Element {
  const agentBridgeRef = useRef<AgentBridge | null>(null);

  /**
   * Initialize agent bridge if not already done.
   */
  const getAgentBridge = useCallback(() => {
    if (!agentBridgeRef.current) {
      agentBridgeRef.current = new AgentBridge();
    }
    return agentBridgeRef.current;
  }, []);

  /**
   * Handle button click - trigger translation.
   */
  const handleClick = useCallback(async () => {
    try {
      onTransformStart('translate');

      const chapterContent = extractChapterContent();
      const chapterId = getChapterId();
      const sessionId = generateSessionId();

      const fullPrompt = TRANSLATE_URDU_PROMPT + chapterContent + '\n\nURDU TRANSLATION:';

      const agentBridge = getAgentBridge();

      agentBridge.setCallbacks({
        onToken: (token: string) => {
          onContentChunk(token);
        },
        onComplete: () => {
          onTransformComplete();
        },
        onError: (error: Error) => {
          onTransformError(error.message || 'Failed to translate content');
        },
      });

      await agentBridge.sendChatMessage(
        fullPrompt,
        chapterId,
        sessionId,
        'anonymous',
        chapterContent
      );
    } catch (error) {
      onTransformError(
        error instanceof Error ? error.message : 'Failed to translate content'
      );
    }
  }, [onTransformStart, onContentChunk, onTransformComplete, onTransformError, getAgentBridge]);

  return (
    <button
      className={`${styles.toolbarButton} ${styles.translateButton}`}
      onClick={handleClick}
      disabled={disabled}
      type="button"
      aria-label="Translate content to Urdu"
      dir="rtl"
    >
      <span className={styles.buttonIcon}>🌐</span>
      <span className={styles.buttonText}>اردو میں ترجمہ</span>
    </button>
  );
}
