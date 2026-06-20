#backend/app/models/promotion.py
from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base

class Promotion(Base):
    __tablename__ = "Promotions"

    PromotionID = Column(Integer, primary_key=True, autoincrement=True)

    PromoCode = Column(String(50))

    DiscountPercent = Column(Numeric(5,2))

    Description = Column(String(255))