from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.user import User  # חובה! אחרת create_all לא יודע עליו
from app.api.v1.users import router as users_router

# יצירת טבלאות במסד
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BizControl API")
app.include_router(users_router, prefix="/api/v1/users")

@app.get("/")
def home():
    return {"message": "API is working!"}
