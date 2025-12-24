/**
 * Types for Personalization & Translation UI Feature
 */

/**
 * Current status of the content transformation process.
 */
export type TransformationStatus = 'idle' | 'loading' | 'streaming' | 'complete' | 'error';

/**
 * Type of transformation being performed.
 */
export type TransformationType = 'personalize' | 'translate' | null;

/**
 * React state for managing the transformation UI.
 */
export interface TransformationState {
  /** Current status of the transformation process */
  status: TransformationStatus;
  /** Type of transformation being performed */
  type: TransformationType;
  /** Accumulated transformed content from streaming response */
  content: string;
  /** Error message if transformation failed */
  error: string | null;
  /** Whether to show the content overlay */
  showOverlay: boolean;
  /** Whether the content is RTL (for Urdu) */
  isRtl: boolean;
}

/**
 * Initial state for transformation.
 */
export const INITIAL_TRANSFORMATION_STATE: TransformationState = {
  status: 'idle',
  type: null,
  content: '',
  error: null,
  showOverlay: false,
  isRtl: false,
};

/**
 * Metadata extracted from current chapter for transformation context.
 */
export interface ChapterMetadata {
  /** Unique identifier for the chapter (from URL or frontmatter) */
  id: string;
  /** Chapter title for display purposes */
  title: string;
  /** Full text content of the chapter (HTML stripped) */
  textContent: string;
  /** Module the chapter belongs to */
  module: string;
}

/**
 * Request payload sent to Agent API for content transformation.
 */
export interface ContentTransformRequest {
  /** The user's query/instruction for the agent */
  userQuery: string;
  /** The chapter ID from which content is being transformed */
  chapterId: string;
  /** Session identifier for the transformation request */
  sessionId: string;
  /** User identifier (can be 'anonymous' for non-authenticated users) */
  userId: string;
  /** The full chapter content to be transformed */
  selectedText: string;
}

/**
 * Props for PersonalizeButton component.
 */
export interface PersonalizeButtonProps {
  onTransformStart: (type: TransformationType) => void;
  onContentChunk: (chunk: string) => void;
  onTransformComplete: () => void;
  onTransformError: (error: string) => void;
  disabled?: boolean;
}

/**
 * Props for TranslateButton component.
 */
export interface TranslateButtonProps {
  onTransformStart: (type: TransformationType) => void;
  onContentChunk: (chunk: string) => void;
  onTransformComplete: () => void;
  onTransformError: (error: string) => void;
  disabled?: boolean;
}

/**
 * Props for ContentOverlay component.
 */
export interface ContentOverlayProps {
  state: TransformationState;
  onClose: () => void;
  onRetry?: () => void;
}

/**
 * Props for BackgroundModal component.
 */
export interface BackgroundModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (background: 'software' | 'hardware') => void;
}
