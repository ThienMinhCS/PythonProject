# backend/app/schemas/flight_seat.py
from pydantic import BaseModel, Field
from typing import Optional

class FlightSeatBase(BaseModel):
    flight_id: int = Field(..., gt=0)
    seat_class_id: int = Field(..., gt=0)
    seat_number: str = Field(..., max_length=10)
    price: float = Field(..., gt=0)
    status: str = Field(default="Available", pattern="^(Available|Reserved|Booked|Maintenance)$")

class FlightSeatCreate(FlightSeatBase):
    pass

class FlightSeatUpdate(BaseModel):
    seat_number: Optional[str] = Field(None, max_length=10)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(Available|Reserved|Booked|Maintenance)$")

class FlightSeatResponse(FlightSeatBase):
    flight_seat_id: int
    
    class Config:
        from_attributes = True