from sqlalchemy import Column, Integer, String
from app.database import Base

class Airport(Base):
    __tablename__ = "Airports"

    AirportID = Column(Integer, primary_key=True, autoincrement=True)

    AirportCode = Column(String(10), unique=True)

    AirportName = Column(String(100))

    City = Column(String(100))

    Country = Column(String(100))