# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# טען את משתני הסביבה מקובץ .env
load_dotenv()

# כתובת מסד הנתונים
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL לא מוגדר. בדקי את קובץ .env שלך"
    )

# יצירת engine של SQLAlchemy
engine = create_engine(DATABASE_URL, future=True)

# יצירת SessionLocal לשימוש ב-Dependency
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# בסיס עבור כל המודלים
Base = declarative_base()

# Dependency להזרקה ל-Routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
