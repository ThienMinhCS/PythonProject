# backend/app/services/pdf_service.py
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from io import BytesIO
from datetime import datetime
import qrcode
from PIL import Image as PILImage
import os

class PDFService:
    @staticmethod
    def generate_boarding_pass(booking_data: dict) -> BytesIO:
        """Tạo vé máy bay dạng PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5276'),
            alignment=1,
            spaceAfter=12
        )
        
        story.append(Paragraph("✈️ BOARDING PASS", title_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Flight Info
        flight_info = booking_data.get('flight', {})
        passenger_info = booking_data.get('passengers', [])
        
        data = [
            ["Đường bay", f"{flight_info.get('departure_city', '')} → {flight_info.get('arrival_city', '')}"],
            ["Mã chuyến bay", flight_info.get('flight_number', 'N/A')],
            ["Ngày khởi hành", flight_info.get('departure_time', 'N/A')],
            ["Giờ khởi hành", flight_info.get('departure_time', 'N/A')],
            ["Giờ đến", flight_info.get('arrival_time', 'N/A')],
            ["Sân bay đi", flight_info.get('departure_airport', 'N/A')],
            ["Sân bay đến", flight_info.get('arrival_airport', 'N/A')],
            ["Số hiệu ghế", flight_info.get('seat_number', 'N/A')],
            ["Hạng ghế", flight_info.get('seat_class', 'Economy')],
        ]
        
        if passenger_info:
            passenger = passenger_info[0] if isinstance(passenger_info, list) else passenger_info
            data.append(["Hành khách", passenger.get('full_name', 'N/A')])
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#d4e6f1')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a5276')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 11),
            ('FONTSIZE', (1, 0), (1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#a9cce3')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # QR Code
        try:
            # Tạo QR code chứa booking info
            qr_data = f"Booking ID: {booking_data.get('booking_id')}\n"
            qr_data += f"Flight: {flight_info.get('flight_number')}\n"
            qr_data += f"Passenger: {passenger_info[0].get('full_name') if passenger_info else 'N/A'}"
            
            qr = qrcode.make(qr_data)
            qr_path = f"temp_qr_{datetime.now().timestamp()}.png"
            qr.save(qr_path)
            
            # Thêm QR vào PDF
            im = Image(qr_path, width=1.5*inch, height=1.5*inch)
            story.append(im)
            
            # Xóa file QR tạm
            if os.path.exists(qr_path):
                os.remove(qr_path)
        except Exception as e:
            print(f"QR Code error: {e}")
        
        story.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph("Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!", footer_style))
        story.append(Paragraph("Hãy đến sân bay trước 2 giờ để làm thủ tục", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer