from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Message
from schemas import MessageCreate, MessageWithUsers, User as UserSchema
from auth import get_current_user
from redis_client import redis_manager
import json

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageWithUsers)
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if receiver exists
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Create message in database
    db_message = Message(
        content=message.content,
        sender_id=current_user.id,
        receiver_id=message.receiver_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Publish message to Redis channel
    channel = redis_manager.get_chat_channel(current_user.id, message.receiver_id)
    message_data = {
        "type": "message",
        "id": db_message.id,
        "content": db_message.content,
        "sender_id": db_message.sender_id,
        "receiver_id": db_message.receiver_id,
        "sender_username": current_user.username,
        "receiver_username": receiver.username,
        "is_read": db_message.is_read,
        "created_at": db_message.created_at.isoformat()
    }
    redis_manager.publish_message(channel, message_data)
    
    # Return message with user details
    return MessageWithUsers(
        id=db_message.id,
        content=db_message.content,
        sender_id=db_message.sender_id,
        receiver_id=db_message.receiver_id,
        is_read=db_message.is_read,
        created_at=db_message.created_at,
        sender=UserSchema(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            is_online=current_user.is_online,
            created_at=current_user.created_at
        ),
        receiver=UserSchema(
            id=receiver.id,
            username=receiver.username,
            email=receiver.email,
            is_online=receiver.is_online,
            created_at=receiver.created_at
        )
    )


@router.get("/conversation/{user_id}", response_model=List[MessageWithUsers])
def get_conversation(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    # Get messages between current user and specified user
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    # Mark messages as read
    for message in messages:
        if message.receiver_id == current_user.id and not message.is_read:
            message.is_read = True
    db.commit()
    
    return messages


@router.get("/search", response_model=List[MessageWithUsers])
def search_messages(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    # Search messages containing the query string
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)) &
        Message.content.contains(q)
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    return messages


@router.put("/{message_id}/read")
def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    
    return {"message": "Message marked as read"}


@router.get("/unread-count")
def get_unread_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(Message).filter(
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).count()
    
    return {"unread_count": count}
