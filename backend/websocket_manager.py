from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import asyncio
from redis_client import redis_manager
from models import User, Message
from sqlalchemy.orm import Session
from database import SessionLocal


class ConnectionManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, WebSocket] = {}
        # Store user info for each connection
        self.user_info: Dict[int, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, username: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_info[user_id] = {"username": username, "user_id": user_id}
        
        # Add user to online users in Redis
        redis_manager.add_online_user(user_id)
        
        # Notify other users that this user is online
        await self.broadcast_user_status(user_id, username, True)
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            if user_id in self.user_info:
                username = self.user_info[user_id]["username"]
                del self.user_info[user_id]
                
                # Remove user from online users in Redis
                redis_manager.remove_online_user(user_id)
                
                # Notify other users that this user is offline
                asyncio.create_task(self.broadcast_user_status(user_id, username, False))
    
    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
    
    async def send_message_to_chat(self, message_data: dict, sender_id: int, receiver_id: int):
        """Send message to both sender and receiver in a 1:1 chat"""
        # Send to sender
        if sender_id in self.active_connections:
            await self.active_connections[sender_id].send_text(json.dumps(message_data))
        
        # Send to receiver
        if receiver_id in self.active_connections:
            await self.active_connections[receiver_id].send_text(json.dumps(message_data))
    
    async def broadcast_user_status(self, user_id: int, username: str, is_online: bool):
        """Broadcast user online/offline status to all connected users"""
        status_message = {
            "type": "user_status",
            "user_id": user_id,
            "username": username,
            "is_online": is_online
        }
        
        for connection in self.active_connections.values():
            try:
                await connection.send_text(json.dumps(status_message))
            except:
                pass  # Connection might be closed
    
    async def send_typing_indicator(self, typing_data: dict, sender_id: int, receiver_id: int):
        """Send typing indicator to chat partner"""
        if receiver_id in self.active_connections:
            await self.active_connections[receiver_id].send_text(json.dumps(typing_data))
    
    async def broadcast_online_users(self, user_id: int):
        """Send list of online users to a specific user"""
        online_users = redis_manager.get_online_users()
        online_user_list = []
        
        # Get user details for online users
        db = SessionLocal()
        try:
            for online_user_id in online_users:
                if int(online_user_id) != user_id:  # Don't include self
                    user = db.query(User).filter(User.id == int(online_user_id)).first()
                    if user:
                        online_user_list.append({
                            "id": user.id,
                            "username": user.username,
                            "is_online": True
                        })
        finally:
            db.close()
        
        message = {
            "type": "online_users",
            "users": online_user_list
        }
        
        await self.send_personal_message(json.dumps(message), user_id)


manager = ConnectionManager()
