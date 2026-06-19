# backend/app/schemas/passenger.py
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional
import re

class PassengerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    date_of_birth: str  # YYYY-MM-DD
    nationality: str = Field(..., max_length=50)
    identifier_type: str = Field(..., pattern="^(Passport|ID Card|Driver License)$")
    identifier_number: str = Field(..., max_length=30)

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        try:
            # Kiểm tra định dạng
            birth_date = datetime.strptime(v, "%Y-%m-%d").date()
            
            # Kiểm tra tuổi (không được nhỏ hơn 0 và không quá 120 tuổi)
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 0:
                raise ValueError("Date of birth cannot be in the future")
            if age > 120:
                raise ValueError("Age cannot be more than 120 years")
            
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    @validator('identifier_number')
    def validate_identifier_number(cls, v, values):
        identifier_type = values.get('identifier_type')
        
        if identifier_type == "Passport":
            # Passport: 1 chữ cái + 7-8 số
            if not re.match(r'^[A-Z][0-9]{7,8}$', v):
                raise ValueError("Passport number must be 1 letter followed by 7-8 digits")
        elif identifier_type == "ID Card":
            # CMND/CCCD: 9 hoặc 12 số
            if not re.match(r'^[0-9]{9}$|^[0-9]{12}$', v):
                raise ValueError("ID Card must be 9 or 12 digits")
        elif identifier_type == "Driver License":
            # Driver License: 8-12 ký tự (chữ và số)
            if not re.match(r'^[A-Z0-9]{8,12}$', v):
                raise ValueError("Driver License must be 8-12 alphanumeric characters")
        
        return v

class PassengerCreate(PassengerBase):
    pass

class PassengerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    date_of_birth: Optional[str] = None
    nationality: Optional[str] = Field(None, max_length=50)
    identifier_type: Optional[str] = Field(None, pattern="^(Passport|ID Card|Driver License)$")
    identifier_number: Optional[str] = Field(None, max_length=30)

class PassengerResponse(PassengerBase):
    passenger_id: int
    
    class Config:
        from_attributes = True

class PassengerWithBooking(PassengerResponse):
    booking_id: Optional[int] = None
    ticket_number: Optional[str] = None
    flight_seat_id: Optional[int] = None