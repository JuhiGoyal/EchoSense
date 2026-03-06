# services/ai_service.py
import os
import requests
import random
from dotenv import load_dotenv

from utils.config import settings

# -----------------------------
# AI Response Service
# -----------------------------
GEMINI_API_KEY = settings.GEMINI_API_KEY
def get_gemini_response(user_message: str, mood: str = "neutral", conversation_history: list = None) -> str:
    """
    Sends the user's message to the Gemini AI API and returns a bot response.
    """
    # Construct prompt with context
    context = f"The user is feeling {mood}."
    if conversation_history:
        context += " Previous conversation:\n" + "\n".join(conversation_history)
    
    full_prompt = f"{context}\n\nUser: {user_message}\n\nAntigravity (AI assistant):"

    if not GEMINI_API_KEY:
        return f"[AI response unavailable] You said: {user_message}"

    try:
        # Correct Gemini API URL (v1beta or v1)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 300,
                "temperature": 0.7
            }
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        # Extract response text based on Gemini API structure
        candidates = data.get("candidates", [])
        if candidates:
            bot_reply = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return bot_reply.strip()
        
        return "I'm here to listen, but I'm having trouble thinking of what to say right now."

    except requests.exceptions.RequestException as e:
        return f"[AI service error] I couldn't reach my brain. ({str(e)})"
    except Exception as e:
        return f"[AI service error] Something went wrong: {str(e)}"


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
