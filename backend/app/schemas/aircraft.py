# backend/app/schemas/aircraft.py
from pydantic import BaseModel, Field
from typing import Optional

class AircraftBase(BaseModel):
    aircraft_code: str = Field(..., max_length=20)
    aircraft_name: str = Field(..., max_length=100)
    total_seats: int = Field(..., ge=1, le=1000)

class AircraftCreate(AircraftBase):
    pass

class AircraftUpdate(BaseModel):
    aircraft_code: Optional[str] = Field(None, max_length=20)
    aircraft_name: Optional[str] = Field(None, max_length=100)
    total_seats: Optional[int] = Field(None, ge=1, le=1000)

class AircraftResponse(AircraftBase):
    aircraft_id: int
    
    class Config:
        from_attributes = True