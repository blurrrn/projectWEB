"""Database models for Delivery Service"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, JSON
from sqlalchemy.sql import func
import enum
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.database import Base


class DeliveryStatus(str, enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"


class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True, index=True)
    user_id = Column(Integer, nullable=False)
    delivery_address = Column(Text, nullable=False)
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING, nullable=False)
    tracking_number = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OutboxMessage(Base):
    """Transaction Outbox pattern"""
    __tablename__ = "outbox_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    occurred_on = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    processed_on = Column(DateTime(timezone=True), nullable=True)
    error = Column(Text, nullable=True)

