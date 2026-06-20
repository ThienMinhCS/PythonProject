#backend/app/models/payment.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "Payments"

    PaymentID = Column(Integer, primary_key=True, autoincrement=True)

    BookingID = Column(Integer, ForeignKey("Bookings.BookingID"))

    Amount = Column(Numeric(18,2))

    PaymentMethod = Column(String(50))

    PaymentDate = Column(DateTime, default=datetime.utcnow)

    Status = Column(String(20))