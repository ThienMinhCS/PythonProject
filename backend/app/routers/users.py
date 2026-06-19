# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services import user_service
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Lấy thông tin user hiện tại"""
    return UserResponse(
        user_id=current_user.UserID,
        full_name=current_user.FullName,
        email=current_user.Email,
        phone=current_user.Phone,
        role=current_user.Role,
        created_at=current_user.CreatedAt
    )

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cập nhật thông tin user hiện tại"""
    return user_service.update_user(db, current_user.UserID, user_update)