from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_all_users(db: Session):
    """Return all users from the database"""
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    """Return a single user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_new_user(db: Session, user_data: UserCreate):
    """Create a new user"""

    # Check for existing email
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Create user object
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        password=get_password_hash(user_data.password),
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Update an existing user"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.first_name is not None:
        user.first_name = user_data.first_name

    if user_data.last_name is not None:
        user.last_name = user_data.last_name

    if user_data.email is not None:
        # Check for email conflict
        existing = (
            db.query(User)
            .filter(
                User.email == user_data.email,
                User.id != user_id
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        user.email = user_data.email

    if user_data.phone is not None:
        user.phone = user_data.phone

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    """Delete a user by ID"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"detail": "User deleted successfully"}
