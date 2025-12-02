import React, { createContext, useContext, useState } from 'react';

const ContextBubbleContext = createContext(null);

export const useContextBubble = () => {
  const context = useContext(ContextBubbleContext);
  if (!context) {
    throw new Error('useContextBubble must be used within a ContextBubbleProvider');
  }
  return context;
};

export const ContextBubbleProvider = ({ children }) => {
  const [selectedContext, setSelectedContext] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const setContext = (context) => {
    setSelectedContext(context);
    setIsExpanded(false); // Collapse by default when new context is set
  };

  const clearContext = () => {
    setSelectedContext(null);
    setIsExpanded(false);
  };

  const toggleExpand = () => {
    setIsExpanded(prev => !prev);
  };

  return (
    <ContextBubbleContext.Provider value={{ selectedContext, setContext, clearContext, isExpanded, toggleExpand }}>
      {children}
    </ContextBubbleContext.Provider>
  );
};

// This file would also contain the logic to render ContextBubble.jsx
// based on the selectedContext state.
