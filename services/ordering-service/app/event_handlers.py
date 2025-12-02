"""Event handlers for Saga orchestration"""
from sqlalchemy.orm import Session
from app.services import handle_payment_completed, handle_shipment_created, handle_shipment_delivered
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def handle_payment_completed_event(message: dict):
    """Handle PaymentCompleted event - update order status"""
    order_id = message.get("order_id")
    
    db = SessionLocal()
    try:
        # Update order status (delivery will be created by delivery service via OrderPaid event)
        handle_payment_completed(db, order_id)
        print(f"Order {order_id} status updated to payment_completed")
    finally:
        db.close()


def handle_shipment_created_event(message: dict):
    """Handle ShipmentCreated event - update order status"""
    order_id = message.get("order_id")
    
    db = SessionLocal()
    try:
        handle_shipment_created(db, order_id)
        print(f"Order {order_id} status updated to shipping")
    finally:
        db.close()


def handle_shipment_delivered_event(message: dict):
    """Handle ShipmentDelivered event - complete order"""
    order_id = message.get("order_id")
    
    db = SessionLocal()
    try:
        handle_shipment_delivered(db, order_id)
        print(f"Order {order_id} completed")
    finally:
        db.close()

