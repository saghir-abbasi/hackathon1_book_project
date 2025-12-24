import React, { useState, useRef, useEffect } from 'react';
import ChatbotButton from './ChatbotButton';
import ChatWindow from './ChatWindow';
import AgentBridge from '../../agent-client/agentBridge'; // Import the AgentBridge

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

  // Use useRef to hold a persistent instance of AgentBridge
  const agentBridgeRef = useRef<AgentBridge | null>(null);

  // Initialize AgentBridge only once
  if (!agentBridgeRef.current) {
    agentBridgeRef.current = new AgentBridge();
  }

  const handleSendMessage = async (text: string) => {
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setIsThinking(true);

    const botMessageId = (Date.now() + 1).toString();
    const initialBotMessage: Message = {
      id: botMessageId,
      text: '',
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, initialBotMessage]);

    // Set up callbacks for the agent bridge
    agentBridgeRef.current.setCallbacks({
      onToken: (token: string) => {
        setMessages((prevMessages) =>
          prevMessages.map((msg) =>
            msg.id === botMessageId ? { ...msg, text: msg.text + token } : msg
          )
        );
      },
      onComplete: () => {
        setIsThinking(false);
      },
      onError: (error: Error) => {
        console.error('Error from stream:', error);
        setMessages((prevMessages) =>
          prevMessages.map((msg) =>
            msg.id === botMessageId ? { ...msg, text: `Sorry, an error occurred: ${error.message}` } : msg
          )
        );
        setIsThinking(false);
      },
      onReconnectAttempt: (attempt: number, delay: number) => {
        console.log(`Reconnect attempt ${attempt} in ${delay}ms...`);
      }
    });

    try {
      // Use AgentBridge to send the message
      await agentBridgeRef.current.sendChatMessage(
        text,
        'chapter-1-placeholder', // Placeholder chapterId
        'session-123-placeholder', // Placeholder sessionId
        'user-abc-placeholder' // Placeholder userId
      );
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === botMessageId ? { ...msg, text: `Sorry, I couldn't connect to the server. ${error.message}` } : msg
        )
      );
      setIsThinking(false);
    }
  };

  return (
    <>
      <ChatbotButton onClick={() => setIsOpen(!isOpen)} isOpen={isOpen} />
      <ChatWindow
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        messages={messages}
        isThinking={isThinking}
        onSendMessage={handleSendMessage}
      />
    </>
  );
};

export default Chatbot;
