# backend/app/services/admin_service.py
from http.client import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from datetime import datetime, timedelta
from app.models import User, Flight, Booking, Payment

def get_dashboard_stats(db: Session) -> Dict:
    """Lấy thống kê cho dashboard admin"""
    # Tổng số users
    total_users = db.query(User).count()
    
    # Tổng số flights
    total_flights = db.query(Flight).count()
    
    # Tổng số bookings
    total_bookings = db.query(Booking).count()
    
    # Doanh thu 30 ngày gần nhất
    thirty_days_ago = datetime.now() - timedelta(days=30)
    revenue = db.query(func.sum(Payment.Amount)).filter(
        Payment.PaymentDate >= thirty_days_ago,
        Payment.Status == "Completed"
    ).scalar() or 0
    
    # Booking theo trạng thái
    booking_status = db.query(
        Booking.Status,
        func.count(Booking.BookingID)
    ).group_by(Booking.Status).all()
    
    return {
        "total_users": total_users,
        "total_flights": total_flights,
        "total_bookings": total_bookings,
        "revenue_last_30_days": float(revenue),
        "booking_status": [{"status": s, "count": c} for s, c in booking_status]
    }

def get_all_users(db: Session, page: int = 1, limit: int = 20) -> Dict:
    """Lấy danh sách users (phân trang)"""
    offset = (page - 1) * limit
    users = db.query(User).offset(offset).limit(limit).all()
    total = db.query(User).count()
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

def update_flight_status(db: Session, flight_id: int, status: str) -> Flight:
    """Cập nhật trạng thái chuyến bay"""
    flight = db.query(Flight).filter(Flight.FlightID == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    flight.Status = status
    db.commit()
    db.refresh(flight)
    return flight