// docusaurus-book-site/src/agent-client/agentBridge.js

import ChatClient from './chatClient';
import StreamHandler from './streamHandler';
import { API_BASE_URL } from './config';

class AgentBridge {
    constructor() {
        this.chatClient = new ChatClient();
        this.streamHandler = null;
        this.messageCallbacks = {
            onToken: (token, isFinal) => console.log("Token:", token, "Final:", isFinal),
            onComplete: () => console.log("Stream complete."),
            onError: (error) => console.error("Stream Error:", error),
            onReconnectAttempt: (attempt, delay) => console.log(`Reconnect attempt ${attempt} in ${delay}ms...`)
        };
    }

    /**
     * Sets the callbacks for handling stream events.
     * @param {object} callbacks - An object containing onToken, onComplete, onError, onReconnectAttempt functions.
     */
    setCallbacks({ onToken, onComplete, onError, onReconnectAttempt }) {
        if (onToken) this.messageCallbacks.onToken = onToken;
        if (onComplete) this.messageCallbacks.onComplete = onComplete;
        if (onError) this.messageCallbacks.onError = onError;
        if (onReconnectAttempt) this.messageCallbacks.onReconnectAttempt = onReconnectAttempt;
    }

    /**
     * Sends a chat message to the AI agent and handles the streaming response.
     * @param {string} userQuery - The user's question or prompt.
     * @param {string} chapterId - The ID of the current book chapter.
     * @param {string} sessionId - The ID of the current chat session.
     * @param {string} userId - The ID of the interacting user.
     * @param {string|null} selectedText - Optional text selected by the user.
     * @param {Array<object>|null} lastModelMessages - Optional last few messages for context.
     */
    async sendChatMessage(userQuery, chapterId, sessionId, userId, selectedText = null, lastModelMessages = null, sectionId = null, offsets = null) {
        // Abort any existing stream before starting a new one
        this.abortStream();

        try {
            const stream = await this.chatClient.sendMessage(
                userQuery, chapterId, sessionId, userId, selectedText, lastModelMessages, sectionId, offsets
            );

            this.streamHandler = new StreamHandler(
                this.chatClient, // Pass the chatClient instance
                this.messageCallbacks.onToken,
                this.messageCallbacks.onComplete,
                this.messageCallbacks.onError,
                this.messageCallbacks.onReconnectAttempt
            );
            await this.streamHandler.handleStream(stream);

        } catch (error) {
            console.error('Failed to initiate chat stream:', error);
            this.messageCallbacks.onError(error);
        }
    }

    /**
     * Aborts the currently active streaming connection.
     */
    abortStream() {
        if (this.streamHandler) {
            this.streamHandler.abort();
            this.streamHandler = null;
        }
        if (this.chatClient) {
            this.chatClient.abortStream();
        }
    }

    /**
     * Fetches metadata from the backend.
     * @returns {Promise<object>} - A promise that resolves to the metadata object.
     */
    async fetchMetadata() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/agent/metadata`, {
                method: 'POST', // or GET, depending on API design
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }

            return response.json();
        } catch (error) {
            console.error('Error fetching metadata:', error);
            throw error;
        }
    }
}

export default AgentBridge;

// Example of how to integrate with a UI component:
// const agentBridge = new AgentBridge();
// agentBridge.setCallbacks({
//     onToken: (token, isFinal) => {
//         // Update UI with token
//         console.log(token);
//     },
//     onComplete: () => {
//         // Update UI to show message complete
//     },
//     onError: (error) => {
//         // Display error message in UI
//     },
//     onReconnectAttempt: (attempt, delay) => {
//         // Show reconnecting indicator in UI
//     }
// });
//
// // Call this from your UI's submit handler
// // agentBridge.sendChatMessage("Explain this concept.", "chapter-id-1", "session-123", "user-456");
