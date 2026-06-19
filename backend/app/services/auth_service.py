# backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.utils.auth import verify_password, get_password_hash, create_access_token, decode_token

def register_user(db: Session, user_data: UserCreate):
    """Đăng ký user mới"""
    existing_user = db.query(User).filter(User.Email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        FullName=user_data.full_name,
        Email=user_data.email,
        PasswordHash=hashed_password,
        Phone=user_data.phone,
        Role="Customer"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token_data = {"sub": str(new_user.UserID), "email": new_user.Email}
    access_token = create_access_token(token_data)
    
    user_response = UserResponse(
        user_id=new_user.UserID,
        full_name=new_user.FullName,
        email=new_user.Email,
        phone=new_user.Phone,
        role=new_user.Role,
        created_at=new_user.CreatedAt
    )
    
    return Token(
        access_token=access_token,
        user=user_response
    )

def login_user(db: Session, user_data: UserLogin):
    """Đăng nhập user"""
    user = db.query(User).filter(User.Email == user_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(user_data.password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token_data = {"sub": str(user.UserID), "email": user.Email}
    access_token = create_access_token(token_data)
    
    user_response = UserResponse(
        user_id=user.UserID,
        full_name=user.FullName,
        email=user.Email,
        phone=user.Phone,
        role=user.Role,
        created_at=user.CreatedAt
    )
    
    return Token(
        access_token=access_token,
        user=user_response
    )

def get_current_user(db: Session, token: str):
    """Lấy user từ token"""
    payload = decode_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.UserID == int(user_id)).first()
    return user