import React, { useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './chatbot.module.css';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  messages: Message[];
  isThinking: boolean;
  onSendMessage: (message: string) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ isOpen, onClose, messages, isThinking, onSendMessage }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className={clsx(styles.chatWindow, isOpen && styles.chatWindowOpen)}>
      <div className={styles.chatHeader}>
        <h3 className={styles.chatTitle}>AI Assistant</h3>
        <button className={styles.chatCloseButton} onClick={onClose} aria-label="Close chat">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className={styles.closeIcon}
          >
            <path
              fillRule="evenodd"
              d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>
      <div className={styles.chatMessages} ref={messagesEndRef}>
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isThinking && (
          <div className={styles.thinkingIndicator}>
            <span>.</span><span>.</span><span>.</span>
          </div>
        )}
      </div>
      <div className={styles.chatInputContainer}>
        <ChatInput onSendMessage={onSendMessage} isThinking={isThinking} />
      </div>
    </div>
  );
};

export default ChatWindow;
