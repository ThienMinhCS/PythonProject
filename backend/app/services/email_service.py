#backend/app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from app.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
    
    def send_email(self, to_email: str, subject: str, body: str, html: bool = False):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_booking_confirmation(self, email: str, booking_id: int, flight_number: str, passengers: List[str]):
        subject = f"Xác nhận đặt vé #{booking_id} - Airline System"
        body = f"""
        <h2>Xác nhận đặt vé thành công!</h2>
        <p>Mã đặt vé: <strong>#{booking_id}</strong></p>
        <p>Chuyến bay: <strong>{flight_number}</strong></p>
        <p>Hành khách: {', '.join(passengers)}</p>
        <p>Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!</p>
        """
        return self.send_email(email, subject, body, html=True)