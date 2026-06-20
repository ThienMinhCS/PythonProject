#backend/app/models/flight.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class Flight(Base):
    __tablename__ = "Flights"

    FlightID = Column(Integer, primary_key=True, autoincrement=True)

    FlightNumber = Column(String(20), unique=True)

    DepartureAirportID = Column(Integer, ForeignKey("Airports.AirportID"))

    ArrivalAirportID = Column(Integer, ForeignKey("Airports.AirportID"))

    AircraftID = Column(Integer, ForeignKey("Aircrafts.AircraftID"))

    DepartureTime = Column(DateTime)

    ArrivalTime = Column(DateTime)

    Status = Column(String(20))