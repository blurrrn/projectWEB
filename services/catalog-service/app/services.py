"""Business logic for Catalog Service"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Flower, Category, Bouquet
from app.schemas import FlowerCreate, FlowerUpdate, CategoryCreate, BouquetCreate
from shared.redis_client import get_cache, set_cache, delete_cache
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


# Flower CRUD
def get_flower(db: Session, flower_id: int):
    """Get flower by ID with cache"""
    cache_key = f"flower:{flower_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    flower = db.query(Flower).filter(Flower.id == flower_id).first()
    if flower:
        flower_dict = {
            "id": flower.id,
            "name": flower.name,
            "description": flower.description,
            "price": float(flower.price),
            "stock_quantity": flower.stock_quantity,
            "flower_type": flower.flower_type.value,
            "image_url": flower.image_url,
            "created_at": flower.created_at.isoformat() if flower.created_at else None,
            "updated_at": flower.updated_at.isoformat() if flower.updated_at else None
        }
        set_cache(cache_key, flower_dict, expire=3600)
        return flower
    return None


def get_flowers(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    """Get list of flowers with cache"""
    cache_key = f"flowers:list:{skip}:{limit}:{search or ''}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    query = db.query(Flower)
    if search:
        query = query.filter(
            or_(
                Flower.name.ilike(f"%{search}%"),
                Flower.description.ilike(f"%{search}%")
            )
        )
    
    flowers = query.offset(skip).limit(limit).all()
    result = [{
        "id": f.id,
        "name": f.name,
        "description": f.description,
        "price": float(f.price),
        "stock_quantity": f.stock_quantity,
        "flower_type": f.flower_type.value,
        "image_url": f.image_url,
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "updated_at": f.updated_at.isoformat() if f.updated_at else None
    } for f in flowers]
    
    set_cache(cache_key, result, expire=300)  # 5 minutes
    return flowers


def create_flower(db: Session, flower: FlowerCreate):
    """Create new flower"""
    db_flower = Flower(**flower.dict())
    db.add(db_flower)
    db.commit()
    db.refresh(db_flower)
    
    # Invalidate cache
    delete_cache(f"flower:{db_flower.id}")
    delete_cache("flowers:list:*")  # Invalidate list cache
    
    return db_flower


def update_flower(db: Session, flower_id: int, flower: FlowerUpdate):
    """Update flower"""
    db_flower = db.query(Flower).filter(Flower.id == flower_id).first()
    if not db_flower:
        return None
    
    update_data = flower.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flower, key, value)
    
    db.commit()
    db.refresh(db_flower)
    
    # Invalidate cache
    delete_cache(f"flower:{flower_id}")
    delete_cache("flowers:list:*")
    
    return db_flower


# Category CRUD
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Get list of categories"""
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate):
    """Create new category"""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Bouquet CRUD
def get_bouquets(db: Session, skip: int = 0, limit: int = 100):
    """Get list of bouquets"""
    return db.query(Bouquet).offset(skip).limit(limit).all()


def get_bouquet(db: Session, bouquet_id: int):
    """Get bouquet by ID"""
    return db.query(Bouquet).filter(Bouquet.id == bouquet_id).first()


def create_bouquet(db: Session, bouquet: BouquetCreate):
    """Create new bouquet"""
    db_bouquet = Bouquet(**bouquet.dict())
    db.add(db_bouquet)
    db.commit()
    db.refresh(db_bouquet)
    return db_bouquet

