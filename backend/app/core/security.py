from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from app.core.config import settings

def get_password_hash(password: str) -> bytes:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password=hashed_password)

def create_access_token(data: dict):
    """
    Create a JWT access token with expiration time in UTC+7 timezone

    """
    to_encode = data.copy()
    bangkok_tz = timezone(timedelta(hours=7))
    expire = datetime.now(bangkok_tz) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)