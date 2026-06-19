# backend/app/routers/flights.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.flight import FlightSearch, FlightResponse
from app.services import flight_service
from app.dependencies import get_current_user

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/search", response_model=List[FlightResponse])
def search_flights(
    departure: str = Query(..., min_length=3, max_length=3),
    arrival: str = Query(..., min_length=3, max_length=3),
    date: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}$'),
    passengers: int = Query(1, ge=1, le=20),
    seat_class: str = Query("Economy"),
    db: Session = Depends(get_db)
):
    """Tìm kiếm chuyến bay"""
    search_params = FlightSearch(
        departure_airport_code=departure,
        arrival_airport_code=arrival,
        departure_date=date,
        passengers=passengers,
        seat_class=seat_class
    )
    return flight_service.search_flights(db, search_params)

@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight_detail(
    flight_id: int,
    db: Session = Depends(get_db)
):
    """Lấy chi tiết chuyến bay"""
    flight = flight_service.get_flight_by_id(db, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight