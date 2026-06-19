# backend/app/schemas/passenger_baggage.py
from pydantic import BaseModel, Field
from typing import Optional

class PassengerBaggageBase(BaseModel):
    passenger_id: int = Field(..., gt=0)
    weight: float = Field(..., ge=0, le=100)  # kg
    price: float = Field(..., ge=0)
    baggage_type: Optional[str] = Field(None, max_length=50)
    is_excess: bool = Field(default=False)

class PassengerBaggageCreate(PassengerBaggageBase):
    pass

class PassengerBaggageUpdate(BaseModel):
    weight: Optional[float] = Field(None, ge=0, le=100)
    price: Optional[float] = Field(None, ge=0)
    baggage_type: Optional[str] = Field(None, max_length=50)
    is_excess: Optional[bool] = None

class PassengerBaggageResponse(PassengerBaggageBase):
    baggage_id: int
    
    class Config:
        from_attributes = True