import React from 'react';
import { useTextSelection } from '../ai/hooks/useTextSelection';
import AskAboutThis from '../ai/components/AskAboutThis'; // Import the new component
import AgentBridge from '../agent-client/agentBridge'; // Import AgentBridge

const agentBridge = new AgentBridge(); // Instantiate AgentBridge once

function Root({ children }) {
  const selection = useTextSelection();

  // Dummy function for now, will be replaced with actual chatbot integration
  const handleAskAboutThis = (selectedContext) => {
    console.log('Ask About This clicked with:', selectedContext);
    // In a real scenario, you'd open the chatbot and prefill the context.
    // For now, we'll simulate sending it to the backend via AgentBridge
    agentBridge.sendChatMessage(
      selectedContext.selectedText,
      selectedContext.chapterId,
      "temp-session-id", // Placeholder
      "temp-user-id",    // Placeholder
      selectedContext.selectedText,
      null,
      selectedContext.sectionId,
      selectedContext.offsets
    ).then(() => console.log("Context sent to backend via AgentBridge"))
     .catch(err => console.error("Error sending context via AgentBridge:", err));
  };

  return (
    <>
      {children}
      <AskAboutThis
        selection={selection}
        onAskAboutThis={handleAskAboutThis}
        isChatbotOpen={false} // Placeholder, will be dynamic
      />
    </>
  );
}

export default Root;
