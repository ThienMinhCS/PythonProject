# backend/app/utils/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import base64
from app.config import settings

def get_password_hash(password: str) -> str:
    """Mã hóa mật khẩu bằng PBKDF2"""
    salt = "airline_salt_2026".encode('utf-8')
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return base64.b64encode(hashed).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu"""
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Giải mã JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None