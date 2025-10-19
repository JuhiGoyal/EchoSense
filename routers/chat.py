# backend/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Chat, User, Diary
from schemas import ChatCreate, ChatResponse, MoodSummary
from datetime import datetime, timedelta
from textblob import TextBlob
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from utils.security import decode_access_token
from services.ai_service import get_gemini_response, get_motivational_quote

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# -----------------------------
# Get current user
# -----------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -----------------------------
# Sentiment Analysis
# -----------------------------
def detect_mood(text: str) -> str:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "happy"
    elif polarity < -0.2:
        return "sad"
    return "neutral"

MOOD_QUOTES = {
    "happy": "Keep smiling! Happiness looks great on you 😊",
    "sad": "Every storm runs out of rain. Stay strong 🌧️",
    "neutral": "Balance is the key to life. Take it easy 😐"
}

# -----------------------------
# POST /chat
# -----------------------------
@router.post("/chat", response_model=ChatResponse)
def create_chat(
    request: ChatCreate,
    diary: bool = False,  # new flag to indicate diary submission
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mood = detect_mood(request.user_message)

    # Include last 5 chats for context
    last_chats = db.query(Chat).filter(Chat.user_id == current_user.id)\
        .order_by(Chat.timestamp.desc()).limit(5).all()
    conversation_history = [f"User: {c.user_message}\nBot: {c.bot_response}" for c in reversed(last_chats)]

    try:
        bot_reply = get_gemini_response(request.user_message, mood, conversation_history)
    except Exception:
        bot_reply = "Sorry, I couldn't process your request at the moment."

    # Save Chat entry
    chat_entry = Chat(
        user_message=request.user_message,
        bot_response=bot_reply,
        mood=mood,
        user_id=current_user.id
    )
    db.add(chat_entry)

    # Save Diary entry if diary flag is True
    if diary:
        diary_entry = Diary(
            text=request.user_message,
            sentiment=mood,
            gemini_response=bot_reply,
            user_id=current_user.id
        )
        db.add(diary_entry)

    db.commit()
    db.refresh(chat_entry)
    return chat_entry

# -----------------------------
# GET /mood-board
# -----------------------------
@router.get("/mood-board")
def get_mood_board(period: str = "weekly", db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    now = datetime.utcnow()
    start_date = now - timedelta(days=7 if period=="weekly" else 30)

    # Fetch last 10 diary entries
    entries = db.query(Diary).filter(
        Diary.user_id == current_user.id,
        Diary.timestamp >= start_date
    ).order_by(Diary.timestamp.desc()).limit(10).all()

    last_10_moods = [e.sentiment for e in entries]

    # Summary for chart
    summary = {}
    for e in entries:
        day = e.timestamp.strftime("%Y-%m-%d")
        if day not in summary:
            summary[day] = {"happy":0,"sad":0,"neutral":0}
        summary[day][e.sentiment.lower()] += 1

    # Dominant mood
    total_happy = sum(v["happy"] for v in summary.values())
    total_sad = sum(v["sad"] for v in summary.values())
    total_neutral = sum(v["neutral"] for v in summary.values())
    dominant = "neutral"
    if total_happy > total_sad and total_happy > total_neutral:
        dominant = "happy"
    elif total_sad > total_happy and total_sad > total_neutral:
        dominant = "sad"

    response = {
        "period": period,
        "summary": summary,
        "dominant_mood": dominant,
        "quote": MOOD_QUOTES.get(dominant, ""),
        "last_10_moods": last_10_moods
    }
    return JSONResponse(content=response)
