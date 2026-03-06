# backend/schemas.py
from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from datetime import datetime
from typing import Optional, List, Dict, Annotated

# Helper to convert MongoDB ObjectId to string
PyObjectId = Annotated[str, BeforeValidator(str)]

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        from_attributes = True

# -----------------------------
# User Schemas
# -----------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase, MongoBaseModel):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# -----------------------------
# Chat Schemas (End-to-End)
# -----------------------------
class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    response: str

class ChatCreate(BaseModel):
    user_message: str

class ChatResponse(MongoBaseModel):
    user_message: str
    bot_response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    mood: Optional[str] = "neutral"

# -----------------------------
# Diary Schemas
# -----------------------------
class DiaryCreateRequest(BaseModel):
    content: str

class DiaryCreate(BaseModel):
    text: str

class DiaryResponse(MongoBaseModel):
    text: str
    sentiment: str
    gemini_response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: PyObjectId

class MoodSummary(BaseModel):
    happy: int
    sad: int
    neutral: int
    period: str
    summary: Dict[str, Dict[str, int]]
    dominant_mood: str
    quote: str
    last_10_moods: List[str]

