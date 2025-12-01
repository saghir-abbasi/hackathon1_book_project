import React, { useState } from 'react';
import clsx from 'clsx';
import styles from '../chatbot.module.css';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isThinking: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isThinking }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isThinking) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.chatInputForm}>
      <textarea
        className={styles.chatInputField}
        placeholder={isThinking ? 'AI is thinking...' : 'Type your message...'}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isThinking}
        rows={1}
      />
      <button
        type="submit"
        className={clsx(styles.chatSendButton, isThinking && styles.chatSendButtonDisabled)}
        disabled={isThinking}
        aria-label="Send message"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className={styles.sendIcon}
        >
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </form>
  );
};

export default ChatInput;
