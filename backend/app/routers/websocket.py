# backend/app/routers/websocket.py
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user_ws
from app.websocket.manager import manager
from app.services import notification_service

async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int = Depends(get_current_user_ws),
    db: Session = Depends(get_db)
):
    await manager.connect(websocket, user_id)
    
    try:
        # Gửi thông báo chưa đọc khi kết nối
        unread = notification_service.get_unread_notifications(db, user_id)
        if unread:
            await websocket.send_json({
                "type": "unread_notifications",
                "data": unread
            })
        
        while True:
            # Nhận message từ client
            data = await websocket.receive_text()
            # Xử lý message nếu cần
            await manager.send_personal_message(user_id, {
                "type": "echo",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)