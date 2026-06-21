# backend/app/services/analytics_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from typing import Dict, List, Any
from app.models import Flight, Booking, Payment, User, Passenger, Airport

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_overview_stats(self) -> Dict:
        """Thống kê tổng quan"""
        total_users = self.db.query(User).count()
        total_flights = self.db.query(Flight).count()
        total_bookings = self.db.query(Booking).count()
        total_revenue = self.db.query(func.sum(Payment.Amount)).filter(
            Payment.Status == "Completed"
        ).scalar() or 0
        
        # Booking trong 24h
        yesterday = datetime.now() - timedelta(days=1)
        bookings_24h = self.db.query(Booking).filter(
            Booking.BookingDate >= yesterday
        ).count()
        
        # Tỷ lệ lấp đầy chuyến bay
        flights = self.db.query(Flight).all()
        avg_load_factor = 0
        if flights:
            total_seats = sum(f.aircraft.TotalSeats for f in flights if f.aircraft)
            total_booked = sum(
                self.db.query(Booking).filter(Booking.FlightID == f.FlightID).count()
                for f in flights
            )
            avg_load_factor = (total_booked / total_seats * 100) if total_seats > 0 else 0
        
        return {
            "total_users": total_users,
            "total_flights": total_flights,
            "total_bookings": total_bookings,
            "total_revenue": float(total_revenue),
            "bookings_24h": bookings_24h,
            "avg_load_factor": round(avg_load_factor, 2)
        }
    
    def get_revenue_by_period(self, period: str = "month") -> List[Dict]:
        """Doanh thu theo thời gian (day/week/month/year)"""
        # period: day, week, month, year
        mapping = {
            "day": (func.DATE(Payment.PaymentDate), "%Y-%m-%d"),
            "week": (func.DATE_TRUNC('week', Payment.PaymentDate), "%Y-W%V"),
            "month": (func.DATE_TRUNC('month', Payment.PaymentDate), "%Y-%m"),
            "year": (func.DATE_TRUNC('year', Payment.PaymentDate), "%Y")
        }
        
        if period not in mapping:
            period = "month"
        
        col, _ = mapping[period]
        results = self.db.query(
            col.label("period"),
            func.sum(Payment.Amount).label("revenue"),
            func.count(Payment.PaymentID).label("count")
        ).filter(
            Payment.Status == "Completed"
        ).group_by(col).order_by(col).all()
        
        return [
            {
                "period": str(r.period) if r.period else "N/A",
                "revenue": float(r.revenue) if r.revenue else 0,
                "count": r.count or 0
            }
            for r in results
        ]
    
    def get_popular_routes(self, limit: int = 10) -> List[Dict]:
        """Các tuyến đường phổ biến nhất"""
        results = self.db.query(
            Flight.DepartureAirportID,
            Flight.ArrivalAirportID,
            func.count(Booking.BookingID).label("bookings")
        ).join(Booking).group_by(
            Flight.DepartureAirportID,
            Flight.ArrivalAirportID
        ).order_by(func.count(Booking.BookingID).desc()).limit(limit).all()
        
        routes = []
        for r in results:
            dep = self.db.query(Airport).filter(Airport.AirportID == r[0]).first()
            arr = self.db.query(Airport).filter(Airport.AirportID == r[1]).first()
            routes.append({
                "from": f"{dep.City} ({dep.AirportCode})" if dep else "N/A",
                "to": f"{arr.City} ({arr.AirportCode})" if arr else "N/A",
                "bookings": r[2] or 0
            })
        return routes
    
    def get_peak_hours(self) -> List[Dict]:
        """Giờ cao điểm đặt vé"""
        results = self.db.query(
            extract('hour', Booking.BookingDate).label("hour"),
            func.count(Booking.BookingID).label("count")
        ).group_by(
            extract('hour', Booking.BookingDate)
        ).order_by(
            extract('hour', Booking.BookingDate)
        ).all()
        
        return [
            {"hour": int(r[0]), "bookings": r[1] or 0}
            for r in results
        ]
    
    def get_user_growth(self, days: int = 30) -> List[Dict]:
        """Tăng trưởng người dùng"""
        start_date = datetime.now() - timedelta(days=days)
        results = self.db.query(
            func.DATE(User.CreatedAt).label("date"),
            func.count(User.UserID).label("count")
        ).filter(
            User.CreatedAt >= start_date
        ).group_by(
            func.DATE(User.CreatedAt)
        ).order_by(
            func.DATE(User.CreatedAt)
        ).all()
        
        return [
            {"date": str(r[0]), "new_users": r[1] or 0}
            for r in results
        ]
    
    def get_booking_status_distribution(self) -> List[Dict]:
        """Phân phối trạng thái booking"""
        results = self.db.query(
            Booking.Status,
            func.count(Booking.BookingID).label("count")
        ).group_by(Booking.Status).all()
        
        return [
            {"status": r[0] or "Unknown", "count": r[1] or 0}
            for r in results
        ]