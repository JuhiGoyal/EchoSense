from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from schemas import UserCreate, UserLogin, UserResponse, Token
from utils.security import hash_password, verify_password, create_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase
import re
from datetime import datetime

router = APIRouter()

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must include an uppercase letter")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must include a lowercase letter")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must include a number")

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing = await db["users"].find_one({
        "$or": [{"email": user.email}, {"username": user.username}]
    })
    
    if existing:
        if existing["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")

    validate_password_strength(user.password)

    user_dict = {
        "username": user.username,
        "email": user.email,
        "password_hash": hash_password(user.password),
        "created_at": datetime.utcnow()
    }
    
    result = await db["users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id

    token = create_access_token({"user_id": str(user_dict["_id"])})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_dict
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"user_id": str(db_user["_id"])})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }
