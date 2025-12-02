import React, { useState, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';

const AskAboutThis = ({ selection, onAskAboutThis, isChatbotOpen }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  const updatePosition = useCallback(() => {
    if (selection && selection.selectedText && selection.selectedText.length > 0) {
      const range = window.getSelection().getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Position the button near the selected text
      // Adjust offset as needed
      const top = rect.top + window.scrollY - 50; // Above selection
      const left = rect.left + window.scrollX + (rect.width / 2) - 75; // Centered horizontally

      setPosition({ top, left });
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  }, [selection]);

  useEffect(() => {
    updatePosition(); // Update on selection change

    const handleScroll = () => {
      // Hide if scrolling, can be optimized to reposition
      setIsVisible(false);
    };

    document.addEventListener('scroll', handleScroll, true);

    return () => {
      document.removeEventListener('scroll', handleScroll, true);
    };
  }, [selection, updatePosition]);

  const handleClick = () => {
    if (onAskAboutThis) {
      onAskAboutThis(selection);
      setIsVisible(false); // Hide button after click
    }
  };

  if (!isVisible || !selection || !selection.selectedText) {
    return null;
  }

  // Use createPortal to render outside the Docusaurus DOM hierarchy
  return createPortal(
    <button
      className="ask-about-this-button"
      style={{
        position: 'absolute',
        top: `${position.top}px`,
        left: `${position.left}px`,
        zIndex: 1000, // Ensure it's above other content
      }}
      onClick={handleClick}
    >
      Ask About This
    </button>,
    document.body // Attach to body
  );
};

export default AskAboutThis;
