# backend/app/websocket/manager.py
from typing import List, Dict, Any
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.user_connections: Dict[int, int] = {}  # user_id -> connection_count
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self.user_connections[user_id] = self.user_connections.get(user_id, 0) + 1
        
        # Gửi thông báo kết nối thành công
        await self.send_personal_message(
            user_id,
            {
                "type": "connection",
                "message": "Connected successfully",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                if user_id in self.user_connections:
                    self.user_connections[user_id] -= 1
                    if self.user_connections[user_id] <= 0:
                        del self.user_connections[user_id]
    
    async def send_personal_message(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error sending message to user {user_id}: {e}")
    
    async def broadcast(self, message: dict, exclude_user_id: int = None):
        for user_id, connections in self.active_connections.items():
            if user_id == exclude_user_id:
                continue
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {e}")
    
    async def send_booking_notification(self, user_id: int, booking_data: dict):
        """Gửi thông báo khi đặt vé thành công"""
        await self.send_personal_message(user_id, {
            "type": "booking_confirmed",
            "data": booking_data,
            "timestamp": datetime.now().isoformat()
        })
    
    async def send_flight_update(self, user_id: int, flight_data: dict):
        """Gửi thông báo khi chuyến bay thay đổi"""
        await self.send_personal_message(user_id, {
            "type": "flight_update",
            "data": flight_data,
            "timestamp": datetime.now().isoformat()
        })
    
    async def send_promotion_notification(self, user_id: int, promotion_data: dict):
        """Gửi thông báo khuyến mãi"""
        await self.send_personal_message(user_id, {
            "type": "new_promotion",
            "data": promotion_data,
            "timestamp": datetime.now().isoformat()
        })

manager = ConnectionManager()