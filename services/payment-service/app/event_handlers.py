"""Event handlers for Payment Service"""
from sqlalchemy.orm import Session
from app.services import process_payment
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def handle_order_created(message: dict):
    """Handle OrderCreated event - process payment"""
    order_id = message.get("order_id")
    user_id = message.get("user_id")
    total_amount = message.get("total_amount")
    
    if not all([order_id, user_id, total_amount]):
        print(f"Invalid OrderCreated message: {message}")
        return
    
    db = SessionLocal()
    try:
        payment = process_payment(db, order_id, user_id, total_amount)
        print(f"Payment processed for order {order_id}: payment_id={payment.id}")
    except Exception as e:
        print(f"Error processing payment for order {order_id}: {e}")
    finally:
        db.close()

