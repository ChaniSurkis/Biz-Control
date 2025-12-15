# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate, UserResponse,UserUpdate
from app.services.user_service import get_all_users, get_user_by_id, create_new_user, delete_user
from app.api.v1.dependencies import get_db
from app.models.user import User
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


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # בדיקת אימייל כפול
    if user_data.email:
        existing = (
            db.query(User)
            .filter(User.email == user_data.email, User.id != user_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data")

    db.refresh(user)
    return user

