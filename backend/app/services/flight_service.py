# backend/app/services/flight_service.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import List, Optional
from app.models import Flight, Airport, FlightSeat, SeatClass, Aircraft
from app.schemas.flight import FlightSearch, FlightResponse

def search_flights(db: Session, search_params: FlightSearch) -> List[FlightResponse]:
    """Tìm kiếm chuyến bay"""
    # Lấy airport IDs
    dep_airport = db.query(Airport).filter(
        Airport.AirportCode == search_params.departure_airport_code
    ).first()
    
    arr_airport = db.query(Airport).filter(
        Airport.AirportCode == search_params.arrival_airport_code
    ).first()
    
    if not dep_airport or not arr_airport:
        return []
    
    # Chuyển đổi date string sang datetime
    dep_date = datetime.strptime(search_params.departure_date, "%Y-%m-%d")
    next_day = dep_date + timedelta(days=1)
    
    # Query flights
    flights = db.query(Flight).filter(
        and_(
            Flight.DepartureAirportID == dep_airport.AirportID,
            Flight.ArrivalAirportID == arr_airport.AirportID,
            Flight.DepartureTime >= dep_date,
            Flight.DepartureTime < next_day,
            Flight.Status == "Scheduled"
        )
    ).all()
    
    results = []
    for flight in flights:
        # Lấy thông tin seat class và price
        seat_class = db.query(SeatClass).filter(
            SeatClass.ClassName == search_params.seat_class
        ).first()
        
        flight_seat = db.query(FlightSeat).filter(
            and_(
                FlightSeat.FlightID == flight.FlightID,
                FlightSeat.SeatClassID == seat_class.SeatClassID
            )
        ).first()
        
        # Lấy thông tin aircraft
        aircraft = db.query(Aircraft).filter(
            Aircraft.AircraftID == flight.AircraftID
        ).first()
        
        if flight_seat and aircraft:
            results.append(FlightResponse(
                flight_id=flight.FlightID,
                flight_number=flight.FlightNumber,
                departure_time=flight.DepartureTime,
                arrival_time=flight.ArrivalTime,
                departure_airport=dep_airport.AirportCode,
                departure_city=dep_airport.City,
                arrival_airport=arr_airport.AirportCode,
                arrival_city=arr_airport.City,
                aircraft_name=aircraft.AircraftName,
                total_seats=aircraft.TotalSeats,
                available_seats=100,  # Cần tính toán
                price=float(flight_seat.Price) if flight_seat.Price else 0,
                status=flight.Status
            ))
    
    return results

def get_flight_by_id(db: Session, flight_id: int) -> Optional[Flight]:
    """Lấy thông tin chi tiết chuyến bay"""
    return db.query(Flight).filter(Flight.FlightID == flight_id).first()