"""Event handlers for Delivery Service"""
from sqlalchemy.orm import Session
from app.services import create_shipment
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def handle_order_paid(message: dict):
    """Handle OrderPaid event - create shipment"""
    order_id = message.get("order_id")
    user_id = message.get("user_id")
    delivery_address = message.get("delivery_address")
    
    if not all([order_id, user_id, delivery_address]):
        print(f"Invalid OrderPaid message: {message}")
        return
    
    db = SessionLocal()
    try:
        shipment = create_shipment(db, order_id, user_id, delivery_address)
        print(f"Shipment created for order {order_id}: shipment_id={shipment.id}, tracking={shipment.tracking_number}")
    except Exception as e:
        print(f"Error creating shipment for order {order_id}: {e}")
    finally:
        db.close()

