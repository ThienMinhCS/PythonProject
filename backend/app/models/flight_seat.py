from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.database import Base

class FlightSeat(Base):
    __tablename__ = "FlightSeats"

    FlightSeatID = Column(Integer, primary_key=True, autoincrement=True)

    FlightID = Column(Integer, ForeignKey("Flights.FlightID"))

    SeatClassID = Column(Integer, ForeignKey("SeatClasses.SeatClassID"))

    SeatNumber = Column(String(10))

    Price = Column(Numeric(18,2))

    Status = Column(String(20))