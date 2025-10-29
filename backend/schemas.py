from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int
    is_online: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    receiver_id: int


class Message(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageWithUsers(Message):
    sender: User
    receiver: User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class OnlineUser(BaseModel):
    id: int
    username: str
    is_online: bool


class TypingIndicator(BaseModel):
    user_id: int
    username: str
    is_typing: bool
    chat_partner_id: int
