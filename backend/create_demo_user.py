#!/usr/bin/env python3
"""
Create a demo user for testing
"""
from database import SessionLocal
from models import User
from auth import get_password_hash

def create_demo_user():
    db = SessionLocal()
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.username == 'demo').first()
        if existing_user:
            print('Demo user already exists!')
            print('Username: demo')
            print('Password: demo123')
            return
        
        # Create demo user
        demo_user = User(
            username='demo',
            email='demo@example.com',
            hashed_password=get_password_hash('demo123')
        )
        db.add(demo_user)
        db.commit()
        
        print('Demo user created successfully!')
        print('Username: demo')
        print('Password: demo123')
        print('Email: demo@example.com')
        
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
