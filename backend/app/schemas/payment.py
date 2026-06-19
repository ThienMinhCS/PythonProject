# backend/app/schemas/payment.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    booking_id: int
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., pattern="^(Credit Card|Debit Card|Bank Transfer|E-Wallet)$")
    status: str = Field(default="Pending", pattern="^(Pending|Completed|Failed|Refunded)$")

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    payment_method: Optional[str] = Field(None, pattern="^(Credit Card|Debit Card|Bank Transfer|E-Wallet)$")
    status: Optional[str] = Field(None, pattern="^(Pending|Completed|Failed|Refunded)$")

class PaymentResponse(PaymentBase):
    payment_id: int
    payment_date: datetime
    
    class Config:
        from_attributes = True