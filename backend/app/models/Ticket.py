from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Ticket(Base):
    __tablename__ = "Tickets"

    TicketID = Column(Integer, primary_key=True, autoincrement=True)

    BookingID = Column(Integer, ForeignKey("Bookings.BookingID"))

    PassengerID = Column(Integer, ForeignKey("Passengers.PassengerID"))

    FlightSeatID = Column(Integer, ForeignKey("FlightSeats.FlightSeatID"))

    TicketNumber = Column(String(30))