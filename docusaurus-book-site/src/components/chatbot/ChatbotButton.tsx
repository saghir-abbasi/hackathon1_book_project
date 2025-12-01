import React from 'react';
import styles from './chatbot.module.css';

interface Props {
  onClick: () => void;
}

const ChatbotButton: React.FC<Props> = ({ onClick }) => {
  return (
    <button className={styles.chatbotButton} onClick={onClick}>
      {/* Using a simple SVG as a placeholder for the robot icon */}
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 8V4H8" />
        <rect x="4" y="12" width="16" height="8" rx="2" />
        <path d="M2 12h2" />
        <path d="M20 12h2" />
        <path d="M12 11v- partículas" />
        <path d="M12 12v-1" />
        <path d="m9 16.5-.5.5" />
        <path d="m15 16.5.5.5" />
      </svg>
    </button>
  );
};

export default ChatbotButton;
