"""Business logic for Auth Service"""
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import User, UserRole
from app.schemas import UserCreate, UserLogin
from shared.jwt_utils import create_access_token
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        role=UserRole.USER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by id"""
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, login: UserLogin) -> Optional[User]:
    """Authenticate user"""
    user = get_user_by_email(db, login.email)
    if not user:
        return None
    if not verify_password(login.password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user


def create_user_token(user: User) -> str:
    """Create JWT token for user"""
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
    return create_access_token(token_data)

