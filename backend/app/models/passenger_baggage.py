#backend/app/models/passenger_baggage.py
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from app.database import Base

class PassengerBaggage(Base):
    __tablename__ = "PassengerBaggages"

    BaggageID = Column(Integer, primary_key=True, autoincrement=True)

    PassengerID = Column(Integer, ForeignKey("Passengers.PassengerID"))

    Weight = Column(Numeric(5,2))

    Price = Column(Numeric(18,2))