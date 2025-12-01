import React, { useState, useRef, useEffect } from 'react';
import ChatbotButton from './ChatbotButton';
import ChatWindow from './ChatWindow';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import styles from './chatbot.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const toggleChatWindow = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setIsThinking(true);

    // Simulate bot response after a delay
    setTimeout(() => {
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: 'This is a placeholder response.', // Placeholder bot response
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
      setIsThinking(false);
    }, 1500); // Simulate a 1.5 second delay
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]); // Scroll to bottom when messages change

  return (
    <div className={styles.chatbotContainer}>
      <ChatbotButton onClick={toggleChatWindow} />
      {isOpen && (
        <ChatWindow onClose={toggleChatWindow}>
          <div className={styles.messageList}>
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isThinking && (
              <div className={`${styles.chatMessage} ${styles.botMessage}`}>
                <div className={styles.messageContent}>Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} /> {/* For auto-scrolling */}
          </div>
          <ChatInput onSendMessage={handleSendMessage} />
        </ChatWindow>
      )}
    </div>
  );
};

export default Chatbot;