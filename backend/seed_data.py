# backend/seed_data.py
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    Airport, Aircraft, SeatClass, Flight, 
    User, FlightSeat
)
# Import từ auth.py đã sửa
from app.utils.auth import get_password_hash
from datetime import datetime, timedelta
import random

def seed_all():
    db = SessionLocal()
    
    try:
        # 1. Tạo Airports
        airports = [
            Airport(AirportCode="SGN", AirportName="Tan Son Nhat International Airport", City="Ho Chi Minh", Country="Vietnam"),
            Airport(AirportCode="HAN", AirportName="Noi Bai International Airport", City="Hanoi", Country="Vietnam"),
            Airport(AirportCode="DAD", AirportName="Da Nang International Airport", City="Da Nang", Country="Vietnam"),
            Airport(AirportCode="CXR", AirportName="Cam Ranh International Airport", City="Nha Trang", Country="Vietnam"),
            Airport(AirportCode="PQC", AirportName="Phu Quoc International Airport", City="Phu Quoc", Country="Vietnam"),
            Airport(AirportCode="BKK", AirportName="Suvarnabhumi Airport", City="Bangkok", Country="Thailand"),
            Airport(AirportCode="SIN", AirportName="Changi Airport", City="Singapore", Country="Singapore"),
        ]
        db.add_all(airports)
        db.commit()
        print("✅ Created airports")
        
        # 2. Tạo Aircrafts
        aircrafts = [
            Aircraft(AircraftCode="B738", AircraftName="Boeing 737-800", TotalSeats=180),
            Aircraft(AircraftCode="A321", AircraftName="Airbus A321", TotalSeats=220),
            Aircraft(AircraftCode="A350", AircraftName="Airbus A350-900", TotalSeats=350),
            Aircraft(AircraftCode="B787", AircraftName="Boeing 787-9 Dreamliner", TotalSeats=290),
        ]
        db.add_all(aircrafts)
        db.commit()
        print("✅ Created aircrafts")
        
        # 3. Tạo Seat Classes
        seat_classes = [
            SeatClass(ClassName="Economy", Description="Standard economy class seating"),
            SeatClass(ClassName="Premium Economy", Description="Enhanced economy with extra legroom"),
            SeatClass(ClassName="Business", Description="Business class with lie-flat seats"),
            SeatClass(ClassName="First Class", Description="Luxury first class suites"),
        ]
        db.add_all(seat_classes)
        db.commit()
        print("✅ Created seat classes")
        
        # 4. Tạo Users - Dùng hàm hash mới
        admin_user = User(
            FullName="Admin System",
            Email="admin@airline.com",
            PasswordHash=get_password_hash("admin123"),  # Đã sửa
            Phone="0900000000",
            Role="Admin"
        )
        db.add(admin_user)
        
        customer_user = User(
            FullName="Nguyen Van A",
            Email="customer@email.com",
            PasswordHash=get_password_hash("customer123"),  # Đã sửa
            Phone="0912345678",
            Role="Customer"
        )
        db.add(customer_user)
        
        test_user = User(
            FullName="Test User",
            Email="test@email.com",
            PasswordHash=get_password_hash("test123"),  # Đã sửa
            Phone="0987654321",
            Role="Customer"
        )
        db.add(test_user)
        db.commit()
        print("✅ Created users")
        
        # 5. Tạo Flights
        flights = []
        today = datetime.now().date()
        
        # Lấy airport IDs
        sgn = db.query(Airport).filter(Airport.AirportCode == "SGN").first()
        han = db.query(Airport).filter(Airport.AirportCode == "HAN").first()
        dad = db.query(Airport).filter(Airport.AirportCode == "DAD").first()
        bkk = db.query(Airport).filter(Airport.AirportCode == "BKK").first()
        sin = db.query(Airport).filter(Airport.AirportCode == "SIN").first()
        
        # Lấy aircraft IDs
        b738 = db.query(Aircraft).filter(Aircraft.AircraftCode == "B738").first()
        a321 = db.query(Aircraft).filter(Aircraft.AircraftCode == "A321").first()
        a350 = db.query(Aircraft).filter(Aircraft.AircraftCode == "A350").first()
        
        # Tạo các chuyến bay
        flight_data = [
            # SGN -> HAN
            {"flight_number": "VN101", "departure": sgn, "arrival": han, "aircraft": b738, 
             "departure_time": datetime.combine(today + timedelta(days=1), datetime.strptime("06:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=1), datetime.strptime("08:00", "%H:%M").time())},
            
            {"flight_number": "VN103", "departure": sgn, "arrival": han, "aircraft": a321,
             "departure_time": datetime.combine(today + timedelta(days=1), datetime.strptime("10:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=1), datetime.strptime("12:00", "%H:%M").time())},
            
            {"flight_number": "VN105", "departure": sgn, "arrival": han, "aircraft": b738,
             "departure_time": datetime.combine(today + timedelta(days=1), datetime.strptime("14:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=1), datetime.strptime("16:00", "%H:%M").time())},
            
            # HAN -> SGN
            {"flight_number": "VN102", "departure": han, "arrival": sgn, "aircraft": b738,
             "departure_time": datetime.combine(today + timedelta(days=1), datetime.strptime("07:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=1), datetime.strptime("09:00", "%H:%M").time())},
            
            # SGN -> DAD
            {"flight_number": "VN201", "departure": sgn, "arrival": dad, "aircraft": a321,
             "departure_time": datetime.combine(today + timedelta(days=1), datetime.strptime("08:30", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=1), datetime.strptime("09:45", "%H:%M").time())},
            
            # SGN -> BKK
            {"flight_number": "VN301", "departure": sgn, "arrival": bkk, "aircraft": a350,
             "departure_time": datetime.combine(today + timedelta(days=2), datetime.strptime("09:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=2), datetime.strptime("10:30", "%H:%M").time())},
            
            # HAN -> SIN
            {"flight_number": "VN401", "departure": han, "arrival": sin, "aircraft": a350,
             "departure_time": datetime.combine(today + timedelta(days=2), datetime.strptime("11:00", "%H:%M").time()),
             "arrival_time": datetime.combine(today + timedelta(days=2), datetime.strptime("15:00", "%H:%M").time())},
        ]
        
        for data in flight_data:
            flight = Flight(
                FlightNumber=data["flight_number"],
                DepartureAirportID=data["departure"].AirportID,
                ArrivalAirportID=data["arrival"].AirportID,
                AircraftID=data["aircraft"].AircraftID,
                DepartureTime=data["departure_time"],
                ArrivalTime=data["arrival_time"],
                Status="Scheduled"
            )
            db.add(flight)
            db.flush()
            flights.append(flight)
        
        db.commit()
        print("✅ Created flights")
        
        # 6. Tạo Flight Seats
        economy = db.query(SeatClass).filter(SeatClass.ClassName == "Economy").first()
        business = db.query(SeatClass).filter(SeatClass.ClassName == "Business").first()
        
        for flight in flights:
            # Economy seats
            for i in range(1, 50):
                flight_seat = FlightSeat(
                    FlightID=flight.FlightID,
                    SeatClassID=economy.SeatClassID,
                    SeatNumber=f"E{i:03d}",
                    Price=random.randint(80, 150) * 1000,
                    Status="Available"
                )
                db.add(flight_seat)
            
            # Business seats
            for i in range(1, 16):
                flight_seat = FlightSeat(
                    FlightID=flight.FlightID,
                    SeatClassID=business.SeatClassID,
                    SeatNumber=f"B{i:03d}",
                    Price=random.randint(200, 400) * 1000,
                    Status="Available"
                )
                db.add(flight_seat)
        
        db.commit()
        print("✅ Created flight seats")
        
        print("\n🎉 Seed data completed successfully!")
        print("\n📝 Test accounts:")
        print("  - Admin: admin@airline.com / admin123")
        print("  - Customer: customer@email.com / customer123")
        print("  - Test: test@email.com / test123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()