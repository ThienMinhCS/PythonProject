# backend/app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Flight, Booking
from app.dependencies import get_current_admin_user
from app.services import admin_service, report_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return admin_service.get_dashboard_stats(db)

@router.get("/users")
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return admin_service.get_all_users(db, page, limit)

@router.put("/flights/{flight_id}/status")
def update_flight_status(
    flight_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    return admin_service.update_flight_status(db, flight_id, status)

@router.get("/reports/revenue")
def get_revenue_report(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    # Parse dates
    from datetime import datetime
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return report_service.ReportService(db).get_revenue_report(start, end)