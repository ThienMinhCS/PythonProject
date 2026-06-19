# backend/app/utils/validators.py
import re
from datetime import datetime
from typing import Optional

def validate_email(email: str) -> bool:
    """Kiểm tra email hợp lệ"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại (Việt Nam)"""
    pattern = r'^(0[3|5|7|8|9])+([0-9]{8})$'
    return re.match(pattern, phone) is not None

def validate_date(date_str: str) -> bool:
    """Kiểm tra định dạng ngày tháng"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_flight_number(flight_number: str) -> bool:
    """Kiểm tra mã chuyến bay (VD: VN123)"""
    pattern = r'^[A-Z]{2}[0-9]{1,4}$'
    return re.match(pattern, flight_number) is not None