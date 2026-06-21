# backend/app/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services import payment_service
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return payment_service.create_payment(db, payment_data, current_user)

@router.get("/booking/{booking_id}", response_model=PaymentResponse)
def get_payment_by_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = payment_service.get_payment_by_booking(db, booking_id, current_user.UserID)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment