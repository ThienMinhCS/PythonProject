# backend/app/services/payment_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models import Payment, Booking, User
from app.schemas.payment import PaymentCreate, PaymentResponse

def create_payment(db: Session, payment_data: PaymentCreate, current_user: User):
    # Kiểm tra booking
    booking = db.query(Booking).filter(
        Booking.BookingID == payment_data.booking_id,
        Booking.UserID == current_user.UserID
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.Status != "Pending":
        raise HTTPException(status_code=400, detail="Booking already paid or cancelled")
    
    # Tạo payment
    payment = Payment(
        BookingID=payment_data.booking_id,
        Amount=payment_data.amount,
        PaymentMethod=payment_data.payment_method,
        PaymentDate=datetime.now(),
        Status="Completed"  # Giả định thanh toán thành công
    )
    db.add(payment)
    
    # Update booking status
    booking.Status = "Confirmed"
    
    db.commit()
    db.refresh(payment)
    
    return PaymentResponse.model_validate(payment)