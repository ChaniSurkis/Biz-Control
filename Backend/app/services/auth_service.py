from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    """Authenticate user by email and password"""
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
