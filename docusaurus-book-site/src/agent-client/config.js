// docusaurus-book-site/src/agent-client/config.js

// Define API_BASE_URL for both server-side and client-side rendering
// Docusaurus uses SSR, so we need to handle both environments
let apiBaseUrl;

// Check if we're in a browser environment (client-side)
if (typeof window !== 'undefined') {
  // Client-side: check hostname
  apiBaseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? "http://localhost:8000"
    : "https://book-project-backend.vercel.app";
} else {
  // Server-side (Node.js environment): assume development for SSR
  apiBaseUrl = "http://localhost:8000";
}

// Ensure API_BASE_URL is never empty as a fallback
if (!apiBaseUrl) {
  apiBaseUrl = "http://localhost:8000"; // Default fallback
}

export const API_BASE_URL = apiBaseUrl;
