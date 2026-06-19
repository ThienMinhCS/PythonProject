# backend/app/routers/promotions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.promotion import (
    PromotionCreate, PromotionResponse, 
    PromotionApplyRequest, PromotionApplyResponse
)
from app.services import promotion_service
from app.dependencies import get_current_user, get_current_admin_user
from app.models import User

router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.post("/apply", response_model=PromotionApplyResponse)
def apply_promotion(
    request: PromotionApplyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Áp dụng mã khuyến mãi"""
    return promotion_service.apply_promotion(db, request.promo_code, request.order_amount)

@router.post("/", response_model=PromotionResponse)
def create_promotion(
    promotion_data: PromotionCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Tạo promotion mới (Admin only)"""
    # Implement create promotion logic
    pass

@router.get("/", response_model=List[PromotionResponse])
def get_all_promotions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách promotions đang active"""
    # Implement get promotions logic
    pass