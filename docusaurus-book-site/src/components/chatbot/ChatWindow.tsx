import React from 'react';
import styles from './chatbot.module.css';

interface Props {
  onClose: () => void;
  children: React.ReactNode;
}

const ChatWindow: React.FC<Props> = ({ onClose, children }) => {
  return (
    <div className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h2>AI Assistant</h2>
        <button onClick={onClose} className={styles.closeButton}>
          {/* Close Icon (X) */}
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <div className={styles.chatBody}>
        {children}
      </div>
    </div>
  );
};

export default ChatWindow;
