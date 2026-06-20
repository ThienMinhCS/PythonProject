#backend/app/models/aircraft.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Aircraft(Base):
    __tablename__ = "Aircrafts"

    AircraftID = Column(Integer, primary_key=True, autoincrement=True)

    AircraftCode = Column(String(20))

    AircraftName = Column(String(100))

    TotalSeats = Column(Integer)