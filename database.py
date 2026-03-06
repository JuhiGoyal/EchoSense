# backend/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

async def get_db():
    """
    FastAPI dependency to get the MongoDB database instance.
    """
    yield db
