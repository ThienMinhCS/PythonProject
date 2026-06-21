# backend/app/services/notification_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict
from app.models import User, Booking

def get_unread_notifications(db: Session, user_id: int) -> List[Dict]:
    """Lấy danh sách thông báo chưa đọc của user"""
    # Tạm thời trả về danh sách rỗng
    # Sau này có thể tích hợp với bảng Notifications
    return []

def create_notification(db: Session, user_id: int, title: str, message: str, type: str = "info"):
    """Tạo thông báo mới"""
    # Tạm thời chỉ in ra console
    print(f"📨 Notification for user {user_id}: {title} - {message}")
    return True

def mark_as_read(db: Session, notification_id: int, user_id: int):
    """Đánh dấu thông báo đã đọc"""
    return True

def get_notifications(db: Session, user_id: int, limit: int = 20) -> List[Dict]:
    """Lấy danh sách thông báo của user"""
    return []