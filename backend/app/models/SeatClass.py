from sqlalchemy import Column, Integer, String
from app.database import Base

class SeatClass(Base):
    __tablename__ = "SeatClasses"

    SeatClassID = Column(Integer, primary_key=True, autoincrement=True)

    ClassName = Column(String(50))

    Description = Column(String(255))