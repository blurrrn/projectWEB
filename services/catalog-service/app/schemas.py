"""Pydantic schemas for Catalog Service"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import FlowerType


class FlowerBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    flower_type: FlowerType
    image_url: Optional[str] = None


class FlowerCreate(FlowerBase):
    pass


class FlowerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    flower_type: Optional[FlowerType] = None
    image_url: Optional[str] = None


class FlowerResponse(FlowerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class BouquetBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class BouquetCreate(BouquetBase):
    pass


class BouquetResponse(BouquetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

