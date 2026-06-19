# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới"""
    return auth_service.register_user(db, user_data)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Đăng nhập - dùng cho OAuth2 (x-www-form-urlencoded)"""
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    return auth_service.login_user(db, user_data)

@router.post("/token", response_model=Token)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Token endpoint cho Swagger OAuth2"""
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    return auth_service.login_user(db, user_data)