# backend/app/dependencies.py
from fastapi import Depends, HTTPException, status,WebSocket
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import auth_service
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Lấy thông tin user hiện tại từ token"""
    user = auth_service.get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.Role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

async def get_current_user_ws(websocket: WebSocket):
    """Lấy user từ token trong WebSocket connection"""
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="Missing token")
    
    # Lấy db session
    db = next(get_db())
    user = auth_service.get_current_user(db, token)
    if not user:
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user.UserID