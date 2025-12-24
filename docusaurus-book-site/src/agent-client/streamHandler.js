// docusaurus-book-site/src/agent-client/streamHandler.js

class StreamHandler {
    constructor(chatClient, onToken, onComplete, onError, onReconnectAttempt) {
        this.chatClient = chatClient; // New: Reference to ChatClient
        this.onToken = onToken; // Callback for each token received
        this.onComplete = onComplete; // Callback when stream completes
        this.onError = onError; // Callback on stream error
        this.onReconnectAttempt = onReconnectAttempt; // Callback for reconnection attempts
        this.reader = null;
        this.isReconnecting = false;
        this.maxReconnectAttempts = 5; // Max attempts before giving up
        this.currentReconnectAttempt = 0;
        this.reconnectDelay = 1000; // Initial delay in ms
    }

    async handleStream(stream) {
        this.reader = stream.getReader();
        this.isReconnecting = false;
        this.currentReconnectAttempt = 0;
        await this._readStream();
    }

    async _readStream() {
        try {
            while (true) {
                const { done, value } = await this.reader.read();
                if (done) {
                    this.onComplete();
                    break;
                }
                
                // Each 'value' here is a parsed object from chatClient.js's ReadableStream
                if (value.token) {
                    this.onToken(value.token, value.is_final);
                }
                if (value.event === 'end') {
                    this.onComplete();
                    break;
                }
                if (value.event === 'error') {
                    this.onError(new Error(value.error || 'Unknown stream error'));
                    break;
                }
            }
        } catch (error) {
            console.error("StreamHandler read error:", error);
            if (error.name === 'AbortError') {
                console.log("Stream reading aborted by user.");
            } else {
                this.onError(error);
                // Attempt to reconnect if not explicitly aborted
                if (!this.isReconnecting && error.name !== 'AbortError') {
                    await this._attemptReconnect(); // Await reconnect logic
                }
            }
        }
    }

    async _attemptReconnect() { // Made async to await chatClient.reconnectStream
        if (this.currentReconnectAttempt < this.maxReconnectAttempts) {
            this.isReconnecting = true;
            this.currentReconnectAttempt++;
            const delay = this.reconnectDelay * (2 ** (this.currentReconnectAttempt - 1));
            console.log(`Attempting to reconnect in ${delay}ms... Attempt ${this.currentReconnectAttempt}`);
            this.onReconnectAttempt(this.currentReconnectAttempt, delay);
            
            await new Promise(resolve => setTimeout(resolve, delay));
            
            try {
                const newStream = await this.chatClient.reconnectStream();
                // If old reader exists and is not done, cancel it to avoid resource leaks
                if (this.reader && !this.reader.closed) {
                    try {
                        this.reader.cancel('Reconnecting...');
                    } catch (e) {
                        console.warn("Failed to cancel old stream reader:", e);
                    }
                }
                this.reader = null; // Clear old reader
                await this.handleStream(newStream); // Re-handle the new stream
                console.log("Stream re-established successfully.");
                this.currentReconnectAttempt = 0; // Reset on success
            } catch (reconnectError) {
                console.error("Failed to re-establish stream:", reconnectError);
                // If reconnect fails, try again (loop continues) or give up
                if (this.currentReconnectAttempt >= this.maxReconnectAttempts) {
                    console.error("Max reconnect attempts reached. Giving up.");
                    this.onError(new Error("Max reconnect attempts reached. Please try a new query."));
                    this.isReconnecting = false;
                } else {
                    this.isReconnecting = false; // Allow next attempt
                    await this._attemptReconnect(); // Recursive call for next retry
                }
            }
        } else {
            console.error("Max reconnect attempts reached. Giving up.");
            this.onError(new Error("Max reconnect attempts reached. Please try a new query."));
            this.isReconnecting = false;
        }
    }

    abort() {
        if (this.reader) {
            this.reader.cancel('Stream aborted by user/system.');
            this.reader = null;
        }
        this.isReconnecting = false;
        // The abortController for the fetch request is managed by chatClient
        // this.abortController = null; // Removed as it's not managed here directly anymore
    }
}

export default StreamHandler;
