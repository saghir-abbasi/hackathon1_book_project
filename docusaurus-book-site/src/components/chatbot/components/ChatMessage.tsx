import React from 'react';
import styles from '../chatbot.module.css';

interface Props {
  message: {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
  };
}

const ChatMessage: React.FC<Props> = ({ message }) => {
  const isUser = message.sender === 'user';
  const messageClass = isUser ? styles.userMessage : styles.botMessage;

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`${styles.chatMessage} ${messageClass}`}>
      <div className={styles.messageContent}>{message.text}</div>
      <div className={styles.messageTime}>{formatTime(message.timestamp)}</div>
    </div>
  );
};

export default ChatMessage;
