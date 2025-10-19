# backend/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# -----------------------------
# User Schemas
# -----------------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# -----------------------------
# Chat Schemas
# -----------------------------
class ChatCreate(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    timestamp: datetime
    mood: Optional[str] = "neutral"

    class Config:
        orm_mode = True


# -----------------------------
# Diary Schemas
# -----------------------------
class DiaryCreate(BaseModel):
    text: str

class DiaryResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    gemini_response: Optional[str]
    timestamp: datetime
    user_id: int  # added

    class Config:
        orm_mode = True

class MoodSummary(BaseModel):
    period: str
    summary: dict
    dominant_mood: str
    quote: str

