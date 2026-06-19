# backend/app/schemas/ticket.py
from pydantic import BaseModel, Field
from typing import Optional

class TicketBase(BaseModel):
    booking_id: int
    passenger_id: int
    flight_seat_id: int
    ticket_number: str = Field(..., max_length=30)

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    ticket_number: Optional[str] = Field(None, max_length=30)

class TicketResponse(TicketBase):
    ticket_id: int
    
    class Config:
        from_attributes = True