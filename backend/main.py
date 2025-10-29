from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
from contextlib import asynccontextmanager

from config import settings
from database import engine, Base
from routers import auth, messages, users
from websocket_manager import manager
from redis_client import redis_manager
from auth import get_current_user
from models import User
from schemas import TypingIndicator


# Create tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Chat App API",
    description="Real-time chat application with WebSockets and Redis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Chat App API is running!"}


@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    # In a real app, you'd validate the JWT token here
    # For now, we'll extract user info from token (simplified)
    try:
        # This is a simplified approach - in production, properly validate JWT
        from jose import jwt
        from config import settings
        
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        
        if not username:
            await websocket.close(code=1008, reason="Invalid token")
            return
            
        # Get user from database
        from database import SessionLocal
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        
        if not user:
            await websocket.close(code=1008, reason="User not found")
            return
            
        await manager.connect(websocket, user.id, user.username)
        
        # Send online users list to the newly connected user
        await manager.broadcast_online_users(user.id)
        
        # Listen for Redis messages
        pubsub = redis_manager.subscribe_to_channel(f"user:{user.id}")
        
        try:
            while True:
                # Check for Redis messages
                message = pubsub.get_message(timeout=0.1)
                if message and message['type'] == 'message':
                    data = json.loads(message['data'])
                    await websocket.send_text(json.dumps(data))
                
                # Check for WebSocket messages from client
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                    message_data = json.loads(data)
                    
                    if message_data.get("type") == "typing":
                        # Handle typing indicator
                        typing_data = message_data
                        chat_partner_id = typing_data.get("chat_partner_id")
                        if chat_partner_id:
                            await manager.send_typing_indicator(
                                typing_data, user.id, chat_partner_id
                            )
                    
                except asyncio.TimeoutError:
                    pass
                    
        except WebSocketDisconnect:
            manager.disconnect(user.id)
            pubsub.close()
            
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1008, reason="Internal error")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
