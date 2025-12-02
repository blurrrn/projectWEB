"""Initialize test data"""
from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.services import get_password_hash
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def init_test_users():
    """Create test users"""
    db = SessionLocal()
    try:
        # Check if users already exist
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
        
        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            user = User(
                email="user@example.com",
                password_hash=get_password_hash("user123"),
                full_name="Test User",
                role=UserRole.USER,
                is_active=True
            )
            db.add(user)
        
        db.commit()
        print("Test users created successfully")
    except Exception as e:
        print(f"Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_test_users()

