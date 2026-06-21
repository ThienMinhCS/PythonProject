# backend/app/services/report_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from app.models import Booking, Payment, Flight
import pandas as pd
from io import BytesIO

class ReportService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_revenue_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Báo cáo doanh thu"""
        payments = self.db.query(Payment).filter(
            Payment.PaymentDate.between(start_date, end_date),
            Payment.Status == "Completed"
        ).all()
        
        total_revenue = sum(float(p.amount) for p in payments)
        total_bookings = len(payments)
        
        return {
            "total_revenue": total_revenue,
            "total_bookings": total_bookings,
            "average_price": total_revenue / total_bookings if total_bookings > 0 else 0,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        }
    
    def export_to_excel(self, data: List[Dict], sheet_name: str = "Report") -> BytesIO:
        """Xuất dữ liệu ra Excel"""
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        output.seek(0)
        return output