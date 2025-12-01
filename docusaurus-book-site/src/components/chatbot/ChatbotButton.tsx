import React from 'react';
import clsx from 'clsx';
import styles from './chatbot.module.css';

interface ChatbotButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

const ChatbotButton: React.FC<ChatbotButtonProps> = ({ onClick, isOpen }) => {
  return (
    <button
      className={clsx(styles.chatbotButton, isOpen && styles.chatbotButtonOpen)}
      onClick={onClick}
      aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className={styles.chatbotIcon}
      >
        {isOpen ? (
          <path
            fillRule="evenodd"
            d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z"
            clipRule="evenodd"
          />
        ) : (
          <path
            fillRule="evenodd"
            d="M4.804 21.213c.716 0 1.411-.082 2.09-.236l.875-1.093a.75.75 0 01.993-.178l2.251 1.126c2.721 0 5.37-1.395 6.943-3.692.21-.303.417-.618.618-.943L19.231 7.66c-.218-.363-.495-.668-.84-.912a7.502 7.502 0 00-6.417-1.761 7.04 7.04 0 00-1.056.082l-.84.21-.496-.989a.75.75 0 00-.91-.355L5.08 3.991A.75.75 0 004 4.67v3.089c0 .408.113.806.325 1.157l1.45 2.535-1.055 1.055a4.782 4.782 0 00-1.314.928c-.464.4-.852.846-1.166 1.343a3.02 3.02 0 00-.596 1.638l-.05.374c0 .329.16.65.447.869l.745.565c.291.22.62.344.957.344zm7.04-10.377a.75.75 0 00-1.06-1.06L8.47 11.94l-1.72-1.72a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.06 0l3.25-3.25z"
            clipRule="evenodd"
          />
        )}
      </svg>
    </button>
  );
};

export default ChatbotButton;
