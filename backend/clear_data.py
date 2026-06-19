# backend/clear_data.py
from app.database import SessionLocal, engine, Base
from app.models import (
    User, Passenger, Airport, Aircraft, Flight, 
    SeatClass, FlightSeat, Booking, Ticket, Payment
)

def clear_all_data():
    db = SessionLocal()
    try:
        # Xóa theo thứ tự (foreign key constraints)
        print("🗑️  Clearing data...")
        
        # Xóa các bảng con trước
        db.query(Ticket).delete()
        db.query(Booking).delete()
        db.query(Payment).delete()
        db.query(FlightSeat).delete()
        db.query(Flight).delete()
        db.query(Passenger).delete()
        db.query(User).delete()
        db.query(Airport).delete()
        db.query(Aircraft).delete()
        db.query(SeatClass).delete()
        
        db.commit()
        print("✅ All data cleared successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_data()