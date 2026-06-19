# backend/app/schemas/seat_class.py
from pydantic import BaseModel, Field
from typing import Optional

class SeatClassBase(BaseModel):
    class_name: str = Field(..., pattern="^(Economy|Premium Economy|Business|First Class)$")
    description: Optional[str] = Field(None, max_length=255)

class SeatClassCreate(SeatClassBase):
    pass

class SeatClassUpdate(BaseModel):
    class_name: Optional[str] = Field(None, pattern="^(Economy|Premium Economy|Business|First Class)$")
    description: Optional[str] = Field(None, max_length=255)

class SeatClassResponse(SeatClassBase):
    seat_class_id: int
    
    class Config:
        from_attributes = True