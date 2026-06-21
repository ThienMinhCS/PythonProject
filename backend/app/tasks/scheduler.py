#backend/app/tasks/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Booking, Flight
from app.services.email_service import EmailService

scheduler = BackgroundScheduler()

def check_pending_bookings():
    """Kiểm tra booking pending quá 30 phút và hủy tự động"""
    db = SessionLocal()
    try:
        cutoff_time = datetime.now() - timedelta(minutes=30)
        pending_bookings = db.query(Booking).filter(
            Booking.Status == "Pending",
            Booking.BookingDate < cutoff_time
        ).all()
        
        for booking in pending_bookings:
            booking.Status = "Cancelled"
            # Giải phóng ghế
            # ... logic giải phóng ghế
            print(f"Cancelled booking #{booking.BookingID}")
        
        db.commit()
    finally:
        db.close()

def update_flight_status():
    """Cập nhật trạng thái chuyến bay"""
    db = SessionLocal()
    try:
        now = datetime.now()
        
        # Chuyến bay đã khởi hành
        flights = db.query(Flight).filter(
            Flight.DepartureTime <= now,
            Flight.Status == "Scheduled"
        ).all()
        for flight in flights:
            flight.Status = "Departed"
        
        # Chuyến bay đã hạ cánh
        flights = db.query(Flight).filter(
            Flight.ArrivalTime <= now,
            Flight.Status == "Departed"
        ).all()
        for flight in flights:
            flight.Status = "Landed"
        
        db.commit()
    finally:
        db.close()

# Schedule tasks
scheduler.add_job(
    check_pending_bookings,
    trigger=IntervalTrigger(minutes=5),
    id='check_pending_bookings'
)

scheduler.add_job(
    update_flight_status,
    trigger=IntervalTrigger(minutes=15),
    id='update_flight_status'
)

def start_scheduler():
    scheduler.start()
