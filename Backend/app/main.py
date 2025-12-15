from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.user import User 
from app.api.v1.users import router as users_router
# from app.api.v1.routes import appointments

# יצירת טבלאות במסד
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BizControl API")
app.include_router(users_router, prefix="/api/v1/users")
# app.include_router(
#     appointments.router,
#     prefix="/api/v1/appointments",
#     tags=["appointments"]
# )

@app.get("/")
def home():
    return {"message": "API is working!"}
