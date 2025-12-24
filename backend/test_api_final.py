#!/usr/bin/env python3
"""
Final working test script for the AI agent API.
Properly handles Server-Sent Events (SSE) even when multiple
data chunks arrive in a single response block and include escaped \n.
"""

import json

import requests


def test_agent_final(
    user_query: str,
    # base_url: str = "https://book-project-backend.vercel.app/",
    #
    base_url: str = "http://localhost:8000/",
):
    """
    Sends a query to the AI agent API and properly processes SSE-style chunks.
    """
    url = f"{base_url}/api/agent/query"

    payload = {
        "userQuery": user_query,
        "chapterId": "test-chapter",
        "sessionId": "test-session",
        "userId": "test-user",
    }

    try:
        print(f"Query: {user_query}")
        print("Response: ", end="", flush=True)

        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}, stream=True
        )

        if response.status_code != 200:
            print(f"\nError: {response.status_code} - {response.text}")
            return

        # Read full response text
        content = response.text

        # Split by real newline, since API sends escaped "\n" inside data
        lines = content.splitlines()

        full_response = ""

        for line in lines:
            line = line.strip()
            if not line.startswith("data:"):
                continue

            # Extract JSON part
            raw_json = line[5:].strip()

            # Remove escaped newlines inside the JSON text
            raw_json = raw_json.replace("\\n", "")

            try:
                data = json.loads(raw_json)

                # Token data
                if "token" in data and data["token"]:
                    print(data["token"], end="", flush=True)
                    full_response += data["token"]

                # Event handling
                elif "event" in data:
                    if data["event"] == "end":
                        print()
                        return full_response

                    elif data["event"] == "error":
                        print(f"\nError from API: {data.get('error', 'Unknown error')}")
                        return None

            except json.JSONDecodeError:
                print(f"\nFailed to parse JSON: {raw_json}")
                continue

        print()
        return full_response

    except requests.exceptions.RequestException as e:
        print(f"\nRequest error: {e}")
        return ""
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return ""


def main():
    print("AI Agent Test Script (Final Version)")
    print("Type 'quit' or 'exit' to exit the program")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nEnter your query: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter a query.")
                continue

            test_agent_final(user_input)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
