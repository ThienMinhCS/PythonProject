# backend/app/schemas/airport.py
from pydantic import BaseModel, Field
from typing import Optional

class AirportBase(BaseModel):
    airport_code: str = Field(..., min_length=3, max_length=3, pattern="^[A-Z]{3}$")
    airport_name: str = Field(..., max_length=100)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)

class AirportCreate(AirportBase):
    pass

class AirportUpdate(BaseModel):
    airport_name: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)

class AirportResponse(AirportBase):
    airport_id: int
    
    class Config:
        from_attributes = True