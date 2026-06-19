from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "Bookings"

    BookingID = Column(Integer, primary_key=True, autoincrement=True)

    UserID = Column(Integer, ForeignKey("Users.UserID"))

    BookingDate = Column(DateTime, default=datetime.utcnow)

    Status = Column(String(20))