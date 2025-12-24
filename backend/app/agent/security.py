from typing import Any # Add this import
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from collections import defaultdict
import time
import os

# Configuration for rate limiting and input validation
# These values should ideally come from environment variables or a config file
RATE_LIMIT_PER_MINUTE = int(os.getenv("AGENT_RATE_LIMIT_PER_MINUTE", "5"))
PROMPT_MAX_LENGTH = int(os.getenv("AGENT_PROMPT_MAX_LENGTH", "1000"))
SELECTED_TEXT_MAX_LENGTH = int(os.getenv("AGENT_SELECTED_TEXT_MAX_LENGTH", "2000"))
OUTPUT_MAX_TOKENS = int(os.getenv("AGENT_OUTPUT_MAX_TOKENS", "1024")) # Not directly enforced here, but noted

# In-memory store for rate limiting (for a single instance)
# In a distributed system, this would be a shared cache (e.g., Redis)
rate_limit_store = defaultdict(lambda: {"count": 0, "timestamp": 0})

class AgentSecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_store = defaultdict(lambda: {"count": 0, "timestamp": 0})

    async def dispatch(self, request: Request, call_next):
        # Apply security measures only to agent-related endpoints
        # Skip security checks for OPTIONS requests (CORS preflight)
        if request.url.path.startswith("/api/agent") and request.method != "OPTIONS":
            # 1. Rate Limiting
            if not self._check_rate_limit(request):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Please try again later."}
                )


        response = await call_next(request)
        return response

    def _check_rate_limit(self, request: Request) -> bool:
        # Basic rate limiting by client IP
        client_ip = request.client.host
        current_time = time.time()
        
        client_data = self.rate_limit_store[client_ip]

        if (current_time - client_data["timestamp"]) > 60:
            client_data["count"] = 1
            client_data["timestamp"] = current_time
            return True
        else:
            client_data["count"] += 1
            if client_data["count"] > RATE_LIMIT_PER_MINUTE:
                return False
            return True

    def _validate_input(self, body: dict[str, Any]) -> bool:
        print(f"DEBUG: Validating input body: {body}") # Debugging print
        # Validate prompt length
        user_query = body.get("userQuery", "")
        if not user_query or len(user_query) > PROMPT_MAX_LENGTH:
            print(f"DEBUG: User query validation failed. Query: '{user_query}', Length: {len(user_query)}")
            return False
        
        # Validate selected text length (optional, can be empty)
        selected_text = body.get("selectedText", "")
        if len(selected_text) > SELECTED_TEXT_MAX_LENGTH:
            print(f"DEBUG: Selected text validation failed. Length: {len(selected_text)}")
            return False
        
        # Validate chapterId (required for context)
        chapter_id = body.get("chapterId", "")
        if not chapter_id or not isinstance(chapter_id, str):
            print(f"DEBUG: Chapter ID validation failed. Chapter ID: '{chapter_id}', Type: {type(chapter_id)}")
            return False
        
        return True

# Example of how to integrate this middleware into a FastAPI app:
# from fastapi import FastAPI
# app = FastAPI()
# app.add_middleware(AgentSecurityMiddleware)
