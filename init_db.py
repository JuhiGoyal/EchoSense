# backend/init_db.py
from database import Base, engine
from models import User, Chat, Voice, Diary  # include Diary
from sqlalchemy import inspect

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")

# Verify tables
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in DB:", tables)
