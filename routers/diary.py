from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import DiaryCreateRequest, DiaryResponse
from routers.deps import get_current_user
from services.sentiment_service import analyze_sentiment
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

router = APIRouter()

@router.post("/diary", response_model=DiaryResponse)
async def create_diary_entry(
    request: DiaryCreateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Creates a new diary entry, runs sentiment analysis, and stores it in MongoDB.
    """
    sentiment = analyze_sentiment(request.content)
    
    diary_entry = {
        "text": request.content,
        "sentiment": sentiment,
        "user_id": current_user["_id"],
        "timestamp": datetime.utcnow()
    }
    
    result = await db["diary_entries"].insert_one(diary_entry)
    diary_entry["_id"] = result.inserted_id
    
    return diary_entry
