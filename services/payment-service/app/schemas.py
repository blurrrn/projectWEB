"""Pydantic schemas for Payment Service"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    amount: float
    status: PaymentStatus
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

