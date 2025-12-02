import React from 'react';

const ContextBubble = ({ text, onRemove, onExpandToggle, isExpanded }) => {
  if (!text) return null;

  const displayLimit = 200; // Limit for collapsed view

  return (
    <div className="context-bubble">
      <div className="context-bubble-header">
        <span className="context-bubble-title">Context from selection:</span>
        <div className="context-bubble-actions">
          {text.length > displayLimit && (
            <button onClick={onExpandToggle} className="context-bubble-action-btn">
              {isExpanded ? 'Collapse' : 'Expand'}
            </button>
          )}
          {onRemove && (
            <button onClick={onRemove} className="context-bubble-action-btn context-bubble-remove-btn">
              &times;
            </button>
          )}
        </div>
      </div>
      <div className="context-bubble-content">
        {isExpanded ? text : `${text.substring(0, displayLimit)}...`}
      </div>
    </div>
  );
};

export default ContextBubble;
