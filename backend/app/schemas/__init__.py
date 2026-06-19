# backend/app/schemas/__init__.py
from .user import (
    UserBase, UserCreate, UserLogin, 
    UserResponse, Token, TokenData
)
from .passenger import (
    PassengerBase, PassengerCreate, PassengerUpdate,
    PassengerResponse, PassengerWithBooking
)
from .flight import FlightSearch, FlightBase, FlightResponse
from .booking import PassengerInfo, BookingCreate, BookingResponse
from .airport import AirportBase, AirportCreate, AirportUpdate, AirportResponse
from .aircraft import AircraftBase, AircraftCreate, AircraftUpdate, AircraftResponse
from .seat_class import SeatClassBase, SeatClassCreate, SeatClassUpdate, SeatClassResponse
from .payment import PaymentBase, PaymentCreate, PaymentUpdate, PaymentResponse
from .ticket import TicketBase, TicketCreate, TicketUpdate, TicketResponse
from .promotion import (
    PromotionBase, PromotionCreate, PromotionUpdate, 
    PromotionResponse, PromotionApplyRequest, PromotionApplyResponse
)
from .passenger_baggage import (
    PassengerBaggageBase, PassengerBaggageCreate, 
    PassengerBaggageUpdate, PassengerBaggageResponse
)
from .flight_seat import (
    FlightSeatBase, FlightSeatCreate, FlightSeatUpdate, FlightSeatResponse
)