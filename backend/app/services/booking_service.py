# backend/app/services/booking_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional
from app.models import (
    Booking, Ticket, Passenger, Flight, FlightSeat, 
    SeatClass, Payment, User
)
from app.schemas.booking import BookingCreate, BookingResponse, PassengerInfo
from app.schemas.passenger import PassengerCreate
from app.services.flight_service import get_flight_by_id
from app.utils.validators import validate_email, validate_phone

def create_booking(db: Session, booking_data: BookingCreate, current_user: User):
    """Tạo đặt vé mới"""
    # 1. Kiểm tra chuyến bay tồn tại
    flight = get_flight_by_id(db, booking_data.flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # 2. Kiểm tra ghế trống
    seat_class = db.query(SeatClass).filter(
        SeatClass.ClassName == booking_data.seat_class
    ).first()
    
    if not seat_class:
        raise HTTPException(status_code=404, detail="Seat class not found")
    
    flight_seat = db.query(FlightSeat).filter(
        FlightSeat.FlightID == flight.FlightID,
        FlightSeat.SeatClassID == seat_class.SeatClassID
    ).first()
    
    if not flight_seat:
        raise HTTPException(status_code=404, detail="Flight seat not found")
    
    # Kiểm tra số lượng ghế còn trống
    # (Cần implement logic kiểm tra số ghế đã đặt)
    
    # 3. Tạo booking
    new_booking = Booking(
        UserID=current_user.UserID,
        BookingDate=datetime.utcnow(),
        Status="Pending"
    )
    db.add(new_booking)
    db.flush()  # Để có BookingID
    
    # 4. Tạo passengers và tickets
    total_amount = 0
    tickets = []
    
    for passenger_info in booking_data.passengers:
        # Tạo passenger
        passenger = Passenger(
            FullName=passenger_info.full_name,
            Gender=passenger_info.gender,
            DateOfBirth=datetime.strptime(passenger_info.date_of_birth, "%Y-%m-%d").date(),
            Nationality=passenger_info.nationality,
            IdentifierType=passenger_info.identifier_type,
            IdentifierNumber=passenger_info.identifier_number
        )
        db.add(passenger)
        db.flush()
        
        # Tạo ticket
        ticket = Ticket(
            BookingID=new_booking.BookingID,
            PassengerID=passenger.PassengerID,
            FlightSeatID=flight_seat.FlightSeatID,
            TicketNumber=f"TKT{datetime.now().strftime('%Y%m%d%H%M%S')}{passenger.PassengerID}"
        )
        db.add(ticket)
        tickets.append(ticket.TicketNumber)
        
        # Tính tổng tiền
        total_amount += float(flight_seat.Price)
    
    # 5. Tạo payment
    payment = Payment(
        BookingID=new_booking.BookingID,
        Amount=total_amount,
        PaymentMethod="Pending",
        PaymentDate=datetime.utcnow(),
        Status="Pending"
    )
    db.add(payment)
    
    # 6. Cập nhật status booking
    new_booking.Status = "Confirmed"
    
    db.commit()
    db.refresh(new_booking)
    
    # 7. Tạo response
    return BookingResponse(
        booking_id=new_booking.BookingID,
        booking_date=new_booking.BookingDate,
        status=new_booking.Status,
        total_amount=total_amount,
        flight_number=flight.FlightNumber,
        departure_time=flight.DepartureTime,
        arrival_time=flight.ArrivalTime,
        passengers=booking_data.passengers,
        tickets=tickets
    )

def get_user_bookings(db: Session, user_id: int) -> List[BookingResponse]:
    """Lấy danh sách đặt vé của user"""
    bookings = db.query(Booking).filter(Booking.UserID == user_id).all()
    
    results = []
    for booking in bookings:
        # Lấy tickets
        tickets = db.query(Ticket).filter(Ticket.BookingID == booking.BookingID).all()
        
        # Lấy passengers
        passengers = []
        ticket_numbers = []
        for ticket in tickets:
            passenger = db.query(Passenger).filter(
                Passenger.PassengerID == ticket.PassengerID
            ).first()
            if passenger:
                passengers.append(PassengerInfo(
                    full_name=passenger.FullName,
                    gender=passenger.Gender,
                    date_of_birth=passenger.DateOfBirth.strftime("%Y-%m-%d"),
                    nationality=passenger.Nationality,
                    identifier_type=passenger.IdentifierType,
                    identifier_number=passenger.IdentifierNumber
                ))
                ticket_numbers.append(ticket.TicketNumber)
        
        # Lấy flight
        if tickets:
            flight_seat = db.query(FlightSeat).filter(
                FlightSeat.FlightSeatID == tickets[0].FlightSeatID
            ).first()
            if flight_seat:
                flight = db.query(Flight).filter(
                    Flight.FlightID == flight_seat.FlightID
                ).first()
                
                # Lấy payment
                payment = db.query(Payment).filter(
                    Payment.BookingID == booking.BookingID
                ).first()
                
                results.append(BookingResponse(
                    booking_id=booking.BookingID,
                    booking_date=booking.BookingDate,
                    status=booking.Status,
                    total_amount=float(payment.Amount) if payment else 0,
                    flight_number=flight.FlightNumber if flight else "",
                    departure_time=flight.DepartureTime if flight else datetime.now(),
                    arrival_time=flight.ArrivalTime if flight else datetime.now(),
                    passengers=passengers,
                    tickets=ticket_numbers
                ))
    
    return results

def get_booking_by_id(db: Session, booking_id: int, user_id: int) -> Optional[BookingResponse]:
    """Lấy chi tiết một đặt vé"""
    booking = db.query(Booking).filter(
        Booking.BookingID == booking_id,
        Booking.UserID == user_id
    ).first()
    
    if not booking:
        return None
    
    # Lấy tickets
    tickets = db.query(Ticket).filter(Ticket.BookingID == booking.BookingID).all()
    
    # Lấy passengers và ticket numbers
    passengers = []
    ticket_numbers = []
    for ticket in tickets:
        passenger = db.query(Passenger).filter(
            Passenger.PassengerID == ticket.PassengerID
        ).first()
        if passenger:
            passengers.append(PassengerInfo(
                full_name=passenger.FullName,
                gender=passenger.Gender,
                date_of_birth=passenger.DateOfBirth.strftime("%Y-%m-%d") if passenger.DateOfBirth else "",
                nationality=passenger.Nationality,
                identifier_type=passenger.IdentifierType,
                identifier_number=passenger.IdentifierNumber
            ))
            ticket_numbers.append(ticket.TicketNumber)
    
    # Lấy flight
    flight = None
    if tickets:
        flight_seat = db.query(FlightSeat).filter(
            FlightSeat.FlightSeatID == tickets[0].FlightSeatID
        ).first()
        if flight_seat:
            flight = db.query(Flight).filter(
                Flight.FlightID == flight_seat.FlightID
            ).first()
    
    # Lấy payment
    payment = db.query(Payment).filter(
        Payment.BookingID == booking.BookingID
    ).first()
    
    return BookingResponse(
        booking_id=booking.BookingID,
        booking_date=booking.BookingDate,
        status=booking.Status,
        total_amount=float(payment.Amount) if payment else 0,
        flight_number=flight.FlightNumber if flight else "",
        departure_time=flight.DepartureTime if flight else datetime.now(),
        arrival_time=flight.ArrivalTime if flight else datetime.now(),
        passengers=passengers,
        tickets=ticket_numbers
    )