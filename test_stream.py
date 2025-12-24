import requests
import json

# Test the streaming endpoint
url = "http://127.0.0.1:8000/api/agent/query"
headers = {"Content-Type": "application/json"}
data = {
    "userQuery": "What is this book about?",
    "chapterId": "module-1-ros2-basics",
    "sessionId": "session-123",
    "userId": "user-abc"
}

print("Making request to:", url)
try:
    response = requests.post(url, headers=headers, json=data, stream=True, timeout=30)
    print(f"Status Code: {response.status_code}")
    print("Response Headers:", dict(response.headers))

    print("\nStreaming response:")
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(f"Line: {line}")

except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")