# backend/chat.py
from fastapi import APIRouter, Depends, Query
from database import get_db
from schemas import ChatCreate, ChatResponse, MoodSummary
from datetime import datetime, timedelta
from routers.deps import get_current_user
from services.ai_service import get_gemini_response
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

router = APIRouter()

from services.sentiment_service import analyze_sentiment

MOOD_QUOTES = {
    "happy": "Keep shining! Happiness looks great on you 😊",
    "sad": "Every storm runs out of rain. Stay strong 🌧️",
    "neutral": "Balance is the key to life. Take it easy 😐"
}

from services.gemini_service import generate_ai_response
from schemas import ChatMessageRequest, ChatMessageResponse

@router.post("/chat")
async def create_chat(
    request: ChatMessageRequest,
    diary: bool = False,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_message = request.message
    mood = analyze_sentiment(user_message)

    try:
        bot_reply = await generate_ai_response(user_message)
    except Exception:
        bot_reply = "I'm having a little trouble connecting right now, but I'm here for you."

    chat_entry = {
        "user_message": user_message,
        "bot_response": bot_reply,
        "mood": mood,
        "user_id": current_user["_id"],
        "timestamp": datetime.utcnow()
    }
    await db["moods"].insert_one(chat_entry)

    if diary:
        diary_entry = {
            "text": user_message,
            "sentiment": mood,
            "gemini_response": bot_reply,
            "user_id": current_user["_id"],
            "timestamp": datetime.utcnow()
        }
        await db["diary_entries"].insert_one(diary_entry)

    return {"response": bot_reply}

@router.get("/mood-board", response_model=MoodSummary)
async def get_mood_board(
    period: str = Query("weekly", pattern="^(weekly|monthly)$"), 
    db: AsyncIOMotorDatabase = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    now = datetime.utcnow()
    days_back = 7 if period == "weekly" else 30
    start_date = now - timedelta(days=days_back)

    cursor = db["diary_entries"].find({
        "user_id": current_user["_id"],
        "timestamp": {"$gte": start_date}
    }).sort("timestamp", -1)
    entries = await cursor.to_list(length=100)

    last_10_moods = [e["sentiment"] for e in entries[:10]]

    summary = {}
    for e in entries:
        day = e["timestamp"].strftime("%Y-%m-%d")
        if day not in summary:
            summary[day] = {"happy": 0, "sad": 0, "neutral": 0}
        mood_key = e["sentiment"].lower() if e["sentiment"].lower() in ["happy", "sad", "neutral"] else "neutral"
        summary[day][mood_key] += 1

    # Aggregate counts for the last 10 entries as requested
    happy_count = sum(1 for e in entries[:10] if e["sentiment"] == "happy")
    sad_count = sum(1 for e in entries[:10] if e["sentiment"] == "sad")
    neutral_count = sum(1 for e in entries[:10] if e["sentiment"] == "neutral")
    
    dominant = "neutral"
    if happy_count > sad_count and happy_count > neutral_count:
        dominant = "happy"
    elif sad_count > happy_count and sad_count > neutral_count:
        dominant = "sad"

    # Return structure matching both user requirements and frontend expectations
    return {
        "happy": happy_count,
        "sad": sad_count,
        "neutral": neutral_count,
        "period": period,
        "summary": summary,
        "dominant_mood": dominant,
        "quote": MOOD_QUOTES.get(dominant, "Stay balanced."),
        "last_10_moods": last_10_moods
    }
