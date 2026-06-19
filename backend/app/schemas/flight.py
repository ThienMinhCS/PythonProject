# backend/app/schemas/flight.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FlightSearch(BaseModel):
    departure_airport_code: str = Field(..., min_length=3, max_length=3)
    arrival_airport_code: str = Field(..., min_length=3, max_length=3)
    departure_date: str  # YYYY-MM-DD
    return_date: Optional[str] = None
    passengers: int = Field(1, ge=1, le=20)
    seat_class: Optional[str] = "Economy"

class FlightBase(BaseModel):
    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    status: str

class FlightResponse(FlightBase):
    flight_id: int
    departure_airport: str
    departure_city: str
    arrival_airport: str
    arrival_city: str
    aircraft_name: str
    total_seats: int
    available_seats: int
    price: float
    
    class Config:
        from_attributes = True