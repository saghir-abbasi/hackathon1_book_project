// docusaurus-book-site/src/agent-client/chatClient.js

import { API_BASE_URL } from "./config"; // Assuming you create a config.js for API_BASE_URL

class ChatClient {
  constructor() {
    this.abortController = null;
    this.maxRetries = 3;
    this.retryDelayBase = 1000; // 1 second
    this.lastPayload = null; // Store the last successfully sent payload
  }

  /**
   * Initiates a new stream connection with the backend.
   * Handles initial fetch retries.
   * @param {object} payload - The message payload to send.
   * @param {number} currentAttempt - Current retry attempt for the initial fetch.
   * @returns {Promise<ReadableStream>} - The ReadableStream from the backend.
   * @throws {Error} If initial fetch fails after max retries or on unrecoverable error.
   */
  async connect(payload, currentAttempt = 0) {
    if (this.abortController) {
      this.abortController.abort(); // Abort previous request if still active
    }
    this.abortController = new AbortController();
    const signal = this.abortController.signal;

    try {
      const response = await fetch(`${API_BASE_URL}/api/agent/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal: signal,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! Status: ${response.status}`,
        );
      }

      // On successful connection, return the stream
      return this._createReadableStream(response);
      //return "hello world";
    } catch (error) {
      if (error.name === "AbortError") {
        console.warn("Connection attempt aborted.");
        throw error; // Propagate abort error
      } else {
        console.error("Error connecting to stream:", error);
        if (currentAttempt < this.maxRetries) {
          const delay = this.retryDelayBase * 2 ** currentAttempt;
          console.log(
            `Retrying connection in ${delay}ms... Attempt ${currentAttempt + 1}`,
          );
          await new Promise((resolve) => setTimeout(resolve, delay));
          return this.connect(payload, currentAttempt + 1); // Recursive retry
        } else {
          throw error; // Propagate error after max retries
        }
      }
    }
  }

  /**
   * Sends a chat message to the AI agent and initiates the streaming response.
   * Stores the payload for potential reconnection.
   * @param {string} userQuery - The user's question or prompt.
   * @param {string} chapterId - The ID of the current book chapter.
   * @param {string} sessionId - The ID of the current chat session.
   * @param {string} userId - The ID of the interacting user.
   * @param {string|null} selectedText - Optional text selected by the user.
   * @param {Array<object>|null} lastModelMessages - Optional last few messages for context.
   * @returns {Promise<ReadableStream>} - The ReadableStream from the backend.
   * @throws {Error} If initial fetch fails after max retries or on unrecoverable error.
   */
  async sendMessage(
    userQuery,
    chapterId,
    sessionId,
    userId,
    selectedText = null,
    lastModelMessages = null,
    sectionId = null,
    offsets = null,
  ) {
    this.lastPayload = {
      userQuery,
      chapterId,
      sessionId,
      userId,
      selectedText,
      lastModelMessages,
      sectionId,
      offsets,
    };
    return this.connect(this.lastPayload);
  }

  /**
   * Attempts to reconnect using the last successfully sent payload.
   * This method is intended to be called by the StreamHandler when a stream breaks.
   * @returns {Promise<ReadableStream>} - The new ReadableStream from the backend.
   * @throws {Error} If no last payload is available or connection fails.
   */
  async reconnectStream() {
    if (!this.lastPayload) {
      throw new Error("No previous message payload found to reconnect with.");
    }
    console.log("Attempting to reconnect stream with last payload.");
    return this.connect(this.lastPayload); // Re-use connect logic for reconnection
  }

  _createReadableStream(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    return new ReadableStream({
      start: (controller) => {
        const push = async () => {
          try {
            const { done, value } = await reader.read();

            if (done) {
              // Process any remaining buffer content when stream is done
              if (buffer.trim()) {
                const lines = buffer.split('\n');
                for (const line of lines) {
                  const trimmedLine = line.trim();
                  if (trimmedLine.startsWith("data: ")) {
                    try {
                      // Remove escaped newlines from the JSON string before parsing
                      const rawJson = trimmedLine.substring(6).replace(/\\n/g, '');
                      const data = JSON.parse(rawJson);
                      controller.enqueue(data); // Enqueue parsed data
                    } catch (e) {
                      console.error("Error parsing SSE data:", e, "Raw line:", trimmedLine);
                    }
                  }
                }
              }
              controller.close();
              return;
            }

            buffer += decoder.decode(value, { stream: true });
            // Split by actual newlines, not double newlines
            const lines = buffer.split('\n');
            // Keep last incomplete line in buffer
            buffer = lines.pop();

            lines.forEach((line) => {
              const trimmedLine = line.trim();
              if (trimmedLine.startsWith("data: ")) {
                try {
                  // Remove escaped newlines from the JSON string before parsing
                  const rawJson = trimmedLine.substring(6).replace(/\\n/g, '');
                  const data = JSON.parse(rawJson);
                  controller.enqueue(data); // Enqueue parsed data
                } catch (e) {
                  console.error("Error parsing SSE data:", e, "Raw line:", trimmedLine);
                }
              }
            });
            push(); // Read next chunk
          } catch (error) {
            if (error.name === "AbortError") {
              console.warn("Stream read aborted.");
            } else {
              console.error("Stream reading error:", error);
              // Do NOT call controller.error here. Let StreamHandler handle errors and reconnection.
            }
          }
        };
        push();
      },
    });
  }

  abortStream() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }
}

export default ChatClient;

// Example usage:
// (async () => {
//     // Ensure API_BASE_URL is defined, e.g., in src/agent-client/config.js
//     // const API_BASE_URL = 'http://localhost:8000';
//     // if (!API_BASE_URL) {
//     //     console.error("API_BASE_URL is not defined in config.js");
//     //     return;
//     // }

//     const chatClient = new ChatClient();
//     try {
//         const stream = await chatClient.sendMessage(
//             "What are the core principles of ROS 2?",
//             "module-1-ros2-basics",
//             "session-123",
//             "user-abc"
//         );

//         const reader = stream.getReader();
//         let result = '';
//         while (true) {
//             const { done, value } = await reader.read();
//             if (done) {
//                 console.log('Stream finished.');
//                 break;
//             }
//             if (value.token) {
//                 result += value.token;
//                 console.log(value.token); // Process token-by-token
//             }
//             if (value.event === 'end') {
//                 console.log('End event received.');
//                 break;
//             }
//             if (value.event === 'error') {
//                 console.error('Error event received:', value.error);
//                 break;
//             }
//         }
//         console.log('Full response:', result);
//     } catch (error) {
//         console.error('Chat failed:', error);
//     }
// })();
