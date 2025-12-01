import React from 'react';
import clsx from 'clsx';
import styles from '../chatbot.module.css';

interface ChatMessageProps {
  message: {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
  };
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div
      className={clsx(styles.chatMessage, {
        [styles.userMessage]: isUser,
        [styles.botMessage]: !isUser,
      })}
    >
      <div className={styles.messageContent}>{message.text}</div>
      <div className={styles.messageTimestamp}>
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default ChatMessage;
