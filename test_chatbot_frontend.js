// Test script to simulate frontend chatbot API call using Node.js built-in modules
const http = require('http');
const https = require('https');

function testChatbotAPI() {
    console.log('Testing chatbot API connection...');

    // Simulate the same request that the frontend would make
    const payload = {
        userQuery: "Hello, can you help me with robotics concepts?",
        chapterId: "module-1-ros2-basics",
        sessionId: "test-session-123",
        userId: "test-user-456"
    };

    const postData = JSON.stringify(payload);

    const options = {
        hostname: 'localhost',
        port: 8000,
        path: '/api/agent/query',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    console.log('Making request to:', `http://${options.hostname}:${options.port}${options.path}`);

    const req = http.request(options, (res) => {
        console.log('Response status:', res.statusCode);
        console.log('Response headers:', res.headers);
        console.log('\nStreaming response from backend:\n');

        let buffer = '';

        res.on('data', (chunk) => {
            buffer += chunk.toString();

            // Process Server-Sent Events
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));
                        console.log('Received data:', data);

                        if (data.token) {
                            process.stdout.write(data.token);
                        }

                        if (data.event === 'end') {
                            console.log('\n\nStream ended properly.');
                        }

                        if (data.event === 'error') {
                            console.error('\nError received:', data.error);
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                        console.log('Raw line:', line);
                    }
                }
            }
        });

        res.on('end', () => {
            console.log('\nStream completed.');
            console.log('Test completed.');
        });
    });

    req.on('error', (e) => {
        console.error('Request error:', e.message);
    });

    // Write data to request body
    req.write(postData);
    req.end();
}

// Run the test
testChatbotAPI();