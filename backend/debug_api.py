#!/usr/bin/env python3
"""
Simple test script to debug the AI agent API
"""

import requests
import json

def test_api_connection():
    # Test basic connectivity
    print("Testing API connection...")

    # Test health endpoint first
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # Test the agent endpoint
    url = "http://localhost:8000/api/agent/query"

    payload = {
        "userQuery": "Hello, can you help me?",
        "chapterId": "test-chapter",
        "sessionId": "test-session",
        "userId": "test-user"
    }

    try:
        print("Sending request to agent endpoint...")
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # Add timeout to prevent hanging
        )

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text[:500]}...")  # First 500 chars

    except requests.exceptions.Timeout:
        print("Request timed out - the server might be processing but not responding quickly")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api_connection()