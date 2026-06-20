#backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True, autoincrement=True)

    FullName = Column(String(100), nullable=False)

    Email = Column(String(100), unique=True, nullable=False)

    PasswordHash = Column(String(255), nullable=False)

    Phone = Column(String(20))

    Role = Column(String(20), default="Customer")

    CreatedAt = Column(DateTime, default=datetime.utcnow)