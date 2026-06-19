# backend/app/schemas/promotion.py
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional
import re

class PromotionBase(BaseModel):
    promo_code: str = Field(..., max_length=50)
    discount_percent: float = Field(..., ge=0, le=100)
    description: Optional[str] = Field(None, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    maximum_discount_amount: Optional[float] = Field(None, ge=0)
    usage_limit: Optional[int] = Field(None, ge=1)
    used_count: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)

    @validator('promo_code')
    def validate_promo_code(cls, v):
        # Promo code: chữ hoa, số, dấu gạch dưới, dấu gạch ngang
        if not re.match(r'^[A-Z0-9_-]{4,30}$', v):
            raise ValueError("Promo code must be 4-30 characters, uppercase letters, numbers, underscore, or hyphen")
        return v

    @validator('end_date')
    def validate_dates(cls, v, values):
        start_date = values.get('start_date')
        if start_date and v and v <= start_date:
            raise ValueError("End date must be after start date")
        return v

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = Field(None, max_length=50)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    description: Optional[str] = Field(None, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    maximum_discount_amount: Optional[float] = Field(None, ge=0)
    usage_limit: Optional[int] = Field(None, ge=1)
    used_count: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class PromotionResponse(PromotionBase):
    promotion_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PromotionApplyRequest(BaseModel):
    promo_code: str
    order_amount: float = Field(..., gt=0)

class PromotionApplyResponse(BaseModel):
    promo_code: str
    discount_percent: float
    discount_amount: float
    final_amount: float
    is_valid: bool
    message: Optional[str] = None
    promotion_id: Optional[int] = None