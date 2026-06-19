# backend/app/schemas/booking.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from .passenger import PassengerCreate

class PassengerInfo(PassengerCreate):
    """Thông tin hành khách khi đặt vé"""
    pass

class BookingCreate(BaseModel):
    flight_id: int = Field(..., gt=0)
    seat_class: str = Field(..., pattern="^(Economy|Premium Economy|Business|First Class)$")
    passengers: List[PassengerInfo] = Field(..., min_items=1, max_items=20)
    promo_code: Optional[str] = Field(None, max_length=50)

    @validator('passengers')
    def validate_passengers_count(cls, v):
        if len(v) > 20:
            raise ValueError("Cannot book more than 20 passengers at once")
        return v

class BookingResponse(BaseModel):
    booking_id: int
    booking_date: datetime
    status: str
    total_amount: float
    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    passengers: List[PassengerInfo]
    tickets: List[str]
    
    class Config:
        from_attributes = True