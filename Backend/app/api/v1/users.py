from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_new_user,
    delete_user,
    update_user
)
from app.db.database import get_db
from app.models.user import User
from app.api.v1.dependencies.auth import require_admin

router = APIRouter(
    tags=["Users"]
)

# -------------------------
# Public – User registration
# -------------------------
@router.post("/", response_model=UserResponse)
def add_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return create_new_user(db, user_data)

# -------------------------
# Admin only
# -------------------------
@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_user_by_id(db, user_id)

@router.delete("/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return delete_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return update_user(db, user_id, user_data)
from app.api.v1.dependencies.auth import get_current_user

@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
