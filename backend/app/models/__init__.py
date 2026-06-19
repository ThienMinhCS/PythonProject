# backend/app/models/__init__.py
from .user import User
from .passenger import Passenger
from .airport import Airport
from .aircraft import Aircraft
from .flight import Flight
from .seat_class import SeatClass
from .flight_seat import FlightSeat
from .booking import Booking
from .ticket import Ticket
from .payment import Payment
from .promotion import Promotion
from .passenger_baggage import PassengerBaggage

__all__ = [
    'User', 'Passenger', 'Airport', 'Aircraft',
    'Flight', 'SeatClass', 'FlightSeat', 'Booking',
    'Ticket', 'Payment', 'Promotion', 'PassengerBaggage'
]