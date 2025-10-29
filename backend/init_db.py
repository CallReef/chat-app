#!/usr/bin/env python3
"""
Initialize the database with sample data
"""
from database import engine, SessionLocal
from models import Base, User
from auth import get_password_hash
import json

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        if db.query(User).first():
            print("Database already initialized")
            return
        
        # Create sample users
        users_data = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "password": "password123"
            },
            {
                "username": "bob",
                "email": "bob@example.com", 
                "password": "password123"
            },
            {
                "username": "charlie",
                "email": "charlie@example.com",
                "password": "password123"
            }
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"])
            )
            db.add(user)
        
        db.commit()
        print("Database initialized with sample users:")
        for user_data in users_data:
            print(f"- {user_data['username']} ({user_data['email']}) - password: {user_data['password']}")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
