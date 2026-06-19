# backend/app/routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services import booking_service
from app.dependencies import get_current_user
from app.models import User
from typing import List  #
router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tạo đặt vé mới"""
    return booking_service.create_booking(db, booking_data, current_user)

@router.get("/my-bookings", response_model=List[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách đặt vé của user"""
    return booking_service.get_user_bookings(db, current_user.UserID)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking_detail(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy chi tiết đặt vé"""
    booking = booking_service.get_booking_by_id(db, booking_id, current_user.UserID)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking