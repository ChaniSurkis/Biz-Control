import os
import hmac
import hashlib
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()


def get_password_hash(password: str) -> str:
    """Hash password using HMAC + SHA256"""
    secret = os.getenv("JWT_SECRET_KEY", "dev-secret")
    return hmac.new(
        key=secret.encode(),
        msg=password.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hash"""
    return hmac.compare_digest(
        get_password_hash(plain_password),
        hashed_password
    )


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
