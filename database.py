# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Provide a safe default for local dev if DATABASE_URL is not set.
# This avoids crashing on startup when .env is missing.
if not DATABASE_URL:
    print("WARNING: DATABASE_URL not found in environment. Falling back to local sqlite:///./echosense.db", file=sys.stderr)
    DATABASE_URL = "sqlite:///./echosense.db"
    connect_args = {"check_same_thread": False}
else:
    # If using sqlite-like URL, we need check_same_thread, else not.
    if DATABASE_URL.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    else:
        connect_args = {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
