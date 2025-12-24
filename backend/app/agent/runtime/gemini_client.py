import google.generativeai as genai
from src.config import settings

class GeminiClient:
    """
    A client for interacting with the Google Gemini API, designed to be a replacement
    for the existing OpenAI client. It encapsulates the logic for streaming chat
    completions from a Gemini model.
    """

    def __init__(self, model_name: str, api_key: str):
        """
        Initializes the Gemini client.
        Configures the `google.generativeai` library with the provided API key and
        initializes the generative model.

        Args:
            model_name (str): The name of the Gemini model to use (e.g., 'gemini-1.5-flash').
            api_key (str): The Google API key for authentication.
        
        Raises:
            ValueError: If the API key is not provided.
        """
        if not api_key:
            raise ValueError("Gemini API key is required.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def stream_chat_completions(self, messages: list, tools: list = None, tool_choice: str = None):
        """
        Initiates a streaming chat session with the Gemini model.

        Args:
            messages (list): A list of message dictionaries to send to the model.
                             Each dictionary should conform to the Gemini API's expected format.
            tools (list, optional): A list of tools the model can use. Defaults to None.
            tool_choice (str, optional): A specific tool to use. Defaults to None.

        Yields:
            str: Chunks of the response text as they are received from the model.
        """
        # The Gemini API's `generate_content` expects a slightly different message format
        # and doesn't have a direct equivalent of OpenAI's `tool_choice`.
        # This implementation focuses on the streaming text generation.
        # Tools would need a more complex adaptation layer.
        
        # Simple conversion from OpenAI-like message format to Gemini's
        # Gemini expects a list of `{'role': 'user'/'model', 'parts': [text]}`
        chat_history = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else msg["role"]
            chat_history.append({"role": role, "parts": [msg["content"]]})
        
        # The last message is the current prompt
        current_prompt = chat_history.pop()["parts"][0]
        
        chat_session = self.model.start_chat(history=chat_history)
        
        response_stream = await chat_session.send_message_async(current_prompt, stream=True)

        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

