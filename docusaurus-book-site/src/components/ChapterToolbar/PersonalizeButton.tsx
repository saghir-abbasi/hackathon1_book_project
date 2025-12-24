import React, { useState, useCallback, useRef } from 'react';
import type { PersonalizeButtonProps } from './types';
import { useUserPreferences } from '@site/src/hooks/useUserPreferences';
import BackgroundModal from './BackgroundModal';
import AgentBridge from '@site/src/agent-client/agentBridge';
import styles from './styles.module.css';

/**
 * Prompt templates for content personalization.
 */
const PERSONALIZE_SOFTWARE_PROMPT = `
You are adapting robotics educational content for a SOFTWARE DEVELOPER audience.

INSTRUCTIONS:
1. Rewrite the content emphasizing software concepts: code patterns, APIs, data structures, algorithms
2. Use analogies from: web development, databases, microservices, cloud computing, DevOps
3. When discussing hardware concepts, explain them in terms a software developer would understand
4. Keep all technical accuracy - just change the framing and examples
5. Maintain the same structure and section headings
6. Output in Markdown format

ORIGINAL CONTENT:
`;

const PERSONALIZE_HARDWARE_PROMPT = `
You are adapting robotics educational content for a HARDWARE ENGINEER audience.

INSTRUCTIONS:
1. Rewrite the content emphasizing hardware concepts: circuits, sensors, actuators, power systems
2. Use analogies from: electronics, embedded systems, control theory, mechanical engineering
3. When discussing software concepts, explain them in terms a hardware engineer would understand
4. Keep all technical accuracy - just change the framing and examples
5. Maintain the same structure and section headings
6. Output in Markdown format

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
  return `personalize-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * PersonalizeButton Component
 *
 * Button that triggers content personalization based on user's background.
 * Shows a modal to select background if not already set.
 */
export default function PersonalizeButton({
  onTransformStart,
  onContentChunk,
  onTransformComplete,
  onTransformError,
  disabled = false,
}: PersonalizeButtonProps): JSX.Element {
  const { background, hasBackground, setBackground } = useUserPreferences();
  const [isModalOpen, setIsModalOpen] = useState(false);
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
   * Perform the personalization transformation.
   */
  const performPersonalization = useCallback(
    async (userBackground: 'software' | 'hardware') => {
      try {
        onTransformStart('personalize');

        const chapterContent = extractChapterContent();
        const chapterId = getChapterId();
        const sessionId = generateSessionId();

        const prompt =
          userBackground === 'software'
            ? PERSONALIZE_SOFTWARE_PROMPT
            : PERSONALIZE_HARDWARE_PROMPT;

        const fullPrompt = prompt + chapterContent + '\n\nPERSONALIZED CONTENT:';

        const agentBridge = getAgentBridge();

        agentBridge.setCallbacks({
          onToken: (token: string) => {
            onContentChunk(token);
          },
          onComplete: () => {
            onTransformComplete();
          },
          onError: (error: Error) => {
            onTransformError(error.message || 'Failed to personalize content');
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
          error instanceof Error ? error.message : 'Failed to personalize content'
        );
      }
    },
    [onTransformStart, onContentChunk, onTransformComplete, onTransformError, getAgentBridge]
  );

  /**
   * Handle button click.
   */
  const handleClick = useCallback(() => {
    if (hasBackground && background) {
      // User already has a background preference, personalize directly
      performPersonalization(background);
    } else {
      // Show modal to select background
      setIsModalOpen(true);
    }
  }, [hasBackground, background, performPersonalization]);

  /**
   * Handle background selection from modal.
   */
  const handleBackgroundSelect = useCallback(
    (selectedBackground: 'software' | 'hardware') => {
      setBackground(selectedBackground);
      setIsModalOpen(false);
      performPersonalization(selectedBackground);
    },
    [setBackground, performPersonalization]
  );

  return (
    <>
      <button
        className={styles.toolbarButton}
        onClick={handleClick}
        disabled={disabled}
        type="button"
        aria-label="Personalize content for your background"
      >
        <span className={styles.buttonIcon}>🎯</span>
        <span className={styles.buttonText}>
          {hasBackground ? `Personalize (${background})` : 'Personalize'}
        </span>
      </button>

      <BackgroundModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSelect={handleBackgroundSelect}
      />
    </>
  );
}
