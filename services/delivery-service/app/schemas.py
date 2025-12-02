"""Pydantic schemas for Delivery Service"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import DeliveryStatus


class ShipmentResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    delivery_address: str
    status: DeliveryStatus
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

