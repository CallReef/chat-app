from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User
from schemas import User as UserSchema, OnlineUser, UserUpdate
from auth import get_current_user
from redis_client import redis_manager

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/online", response_model=List[OnlineUser])
def get_online_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    online_user_ids = redis_manager.get_online_users()
    online_users = []
    
    for user_id in online_user_ids:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user and user.id != current_user.id:  # Don't include self
            online_users.append(OnlineUser(
                id=user.id,
                username=user.username,
                is_online=True
            ))
    
    return online_users


@router.get("/", response_model=List[UserSchema])
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.id != current_user.id).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if username is already taken by another user
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Update user fields
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
