# app/api/v1/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import get_all_users, get_user_by_id, create_new_user, delete_user
from app.api.v1.dependencies import get_db

router = APIRouter()

# GET כל המשתמשים
@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# GET משתמש לפי ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

# POST - יצירת משתמש חדש
@router.post("/", response_model=UserResponse)
def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(db, user_data)

# DELETE - מחיקת משתמש לפי ID
@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
