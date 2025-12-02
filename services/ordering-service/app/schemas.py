"""Pydantic schemas for Ordering Service"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models import OrderStatus


class OrderItemCreate(BaseModel):
    flower_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_address: str


class OrderItemResponse(BaseModel):
    id: int
    flower_id: int
    quantity: int
    price: float
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    delivery_address: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

