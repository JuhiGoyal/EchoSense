# services/ai_service.py
import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# AI Response Service
# -----------------------------
def get_gemini_response(user_message: str, mood: str = "neutral", conversation_history: list = None) -> str:
    """
    Sends the user's message to the Gemini AI API and returns a bot response.
    Handles missing API key safely and provides fallback.

    Parameters:
        user_message (str): Text input from user.
        mood (str): Optional mood context (happy, sad, neutral).
        conversation_history (list of str): Previous conversation messages.

    Returns:
        str: Bot response.
    """
    # Prepare conversation context
    context_text = f"User mood: {mood}"
    if conversation_history:
        context_text += "\nPrevious conversation:\n" + "\n".join(conversation_history)

    if not GEMINI_API_KEY:
        # Fallback for dev if API key missing
        return f"[AI response unavailable] You said: {user_message}"

    try:
        payload = {
            "prompt": user_message,
            "context": context_text,
            "max_tokens": 150
        }

        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        # Replace with actual Gemini API endpoint
        GEMINI_API_URL = "https://gemini.example.com/v1/chat/completions"

        response = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        bot_reply = data.get("choices", [{}])[0].get("text", "")
        if not bot_reply:
            bot_reply = "Sorry, I couldn't generate a response."

        return bot_reply

    except requests.exceptions.RequestException as e:
        return f"[AI service error] Could not fetch response. ({str(e)})"
    except Exception as e:
        return f"[AI service error] Unexpected error: {str(e)}"


# -----------------------------
# Motivational Quotes
# -----------------------------
MOTIVATIONAL_QUOTES = {
    "happy": [
        "Keep shining! Happiness looks great on you.",
        "Your positivity is contagious. Keep it up!"
    ],
    "sad": [
        "Every storm passes. You will feel better soon.",
        "Tough times don't last, but you do!"
    ],
    "neutral": [
        "Every day is a chance to start something new.",
        "Keep going! Little steps lead to big changes."
    ]
}

def get_motivational_quote(mood: str) -> str:
    """
    Returns a motivational quote based on the user's dominant mood.
    """
    mood = mood if mood in MOTIVATIONAL_QUOTES else "neutral"
    return random.choice(MOTIVATIONAL_QUOTES[mood])
