import google.generativeai as genai
from utils.config import settings
import os
import anyio

# Initialize Gemini SDK
genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_ai_response(user_message: str) -> str:
    """
    Generates a response from Gemini AI based on the user's message.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        # Wrapping synchronous call in a thread to prevent blocking
        response = await anyio.to_thread.run_sync(model.generate_content, user_message)
        if response and response.text:
            return response.text
        return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        return "I'm having trouble connecting to my brain right now. Please try again later."
