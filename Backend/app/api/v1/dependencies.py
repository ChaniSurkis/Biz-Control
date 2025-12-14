from sqlalchemy.orm import Session
from app.db.database import SessionLocal

# פונקציה שתספק סשן למסד נתונים
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
