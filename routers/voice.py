# backend/voice.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from database import get_db
from routers.deps import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
import speech_recognition as sr
import tempfile
import os
from datetime import datetime

router = APIRouter()

@router.post("/speech-to-text")
async def speech_to_text(
    file: UploadFile = File(...), 
    db: AsyncIOMotorDatabase = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Convert uploaded audio to text using Google Speech Recognition.
    """
    if not file.filename.endswith((".wav", ".mp3", ".webm", ".ogg")):
        raise HTTPException(status_code=400, detail="Invalid audio format")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Save to MongoDB
        voice_entry = {
            "audio_text": text,
            "user_id": current_user["_id"],
            "timestamp": datetime.utcnow()
        }
        result = await db["voices"].insert_one(voice_entry)

        return {"text": text, "voice_id": str(result.inserted_id)}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Speech recognition service error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
