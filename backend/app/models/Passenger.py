#backend/app/models/passenger.py
from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Passenger(Base):
    __tablename__ = "Passengers"

    PassengerID = Column(Integer, primary_key=True, autoincrement=True)

    FullName = Column(String(100), nullable=False)

    Gender = Column(String(10))

    DateOfBirth = Column(Date)

    Nationality = Column(String(50))

    IdentifierType = Column(String(20))

    IdentifierNumber = Column(String(30))