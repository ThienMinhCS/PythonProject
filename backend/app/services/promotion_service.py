# backend/app/services/promotion_service.py (thêm mới)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models import Promotion
from app.schemas.promotion import PromotionApplyRequest, PromotionApplyResponse

def apply_promotion(db: Session, promo_code: str, order_amount: float) -> PromotionApplyResponse:
    """Áp dụng mã khuyến mãi"""
    # Tìm promotion
    promotion = db.query(Promotion).filter(
        Promotion.PromoCode == promo_code,
        Promotion.IsActive == True
    ).first()
    
    if not promotion:
        return PromotionApplyResponse(
            promo_code=promo_code,
            discount_percent=0,
            discount_amount=0,
            final_amount=order_amount,
            is_valid=False,
            message="Invalid or inactive promotion code"
        )
    
    # Kiểm tra thời gian
    now = datetime.utcnow()
    if promotion.StartDate and promotion.StartDate > now:
        return PromotionApplyResponse(
            promo_code=promo_code,
            discount_percent=0,
            discount_amount=0,
            final_amount=order_amount,
            is_valid=False,
            message="Promotion has not started yet"
        )
    
    if promotion.EndDate and promotion.EndDate < now:
        return PromotionApplyResponse(
            promo_code=promo_code,
            discount_percent=0,
            discount_amount=0,
            final_amount=order_amount,
            is_valid=False,
            message="Promotion has expired"
        )
    
    # Kiểm tra usage limit
    if promotion.UsageLimit and promotion.UsedCount >= promotion.UsageLimit:
        return PromotionApplyResponse(
            promo_code=promo_code,
            discount_percent=0,
            discount_amount=0,
            final_amount=order_amount,
            is_valid=False,
            message="Promotion usage limit has been reached"
        )
    
    # Kiểm tra minimum order amount
    if promotion.MinimumOrderAmount and order_amount < promotion.MinimumOrderAmount:
        return PromotionApplyResponse(
            promo_code=promo_code,
            discount_percent=0,
            discount_amount=0,
            final_amount=order_amount,
            is_valid=False,
            message=f"Minimum order amount is {promotion.MinimumOrderAmount}"
        )
    
    # Tính toán discount
    discount_amount = order_amount * (promotion.DiscountPercent / 100)
    
    # Giới hạn maximum discount
    if promotion.MaximumDiscountAmount and discount_amount > promotion.MaximumDiscountAmount:
        discount_amount = promotion.MaximumDiscountAmount
    
    final_amount = order_amount - discount_amount
    
    return PromotionApplyResponse(
        promo_code=promo_code,
        discount_percent=promotion.DiscountPercent,
        discount_amount=discount_amount,
        final_amount=final_amount,
        is_valid=True,
        message="Promotion applied successfully",
        promotion_id=promotion.PromotionID
    )

def increment_promotion_usage(db: Session, promotion_id: int):
    """Tăng số lần sử dụng promotion"""
    promotion = db.query(Promotion).filter(Promotion.PromotionID == promotion_id).first()
    if promotion:
        promotion.UsedCount = (promotion.UsedCount or 0) + 1
        db.commit()
        db.refresh(promotion)
    return promotion