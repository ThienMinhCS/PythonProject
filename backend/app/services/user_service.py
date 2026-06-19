# backend/app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.schemas.user import UserResponse
from app.utils.auth import get_password_hash

def update_user(db: Session, user_id: int, user_data: dict):
    """Cập nhật thông tin user"""
    user = db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Cập nhật các field
    if "full_name" in user_data:
        user.FullName = user_data["full_name"]
    if "phone" in user_data:
        user.Phone = user_data["phone"]
    if "password" in user_data:
        user.PasswordHash = get_password_hash(user_data["password"])
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)

def get_user_by_id(db: Session, user_id: int):
    """Lấy user theo ID"""
    return db.query(User).filter(User.UserID == user_id).first()