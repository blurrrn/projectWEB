"""Business logic for Payment Service"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Payment, PaymentStatus, OutboxMessage
from shared.rabbitmq_client import publish_message
import uuid
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def process_payment(db: Session, order_id: int, user_id: int, amount: float):
    """Process payment for order"""
    # Create payment
    payment = Payment(
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        status=PaymentStatus.PROCESSING,
        transaction_id=str(uuid.uuid4())
    )
    db.add(payment)
    db.flush()
    
    # Simulate payment processing (in real app would call payment gateway)
    # For demo, always succeed
    payment.status = PaymentStatus.COMPLETED
    db.flush()
    
    # Create outbox message
    outbox_message = OutboxMessage(
        event_type="PaymentCompleted",
        payload={
            "payment_id": payment.id,
            "order_id": order_id,
            "user_id": user_id,
            "amount": float(amount),
            "transaction_id": payment.transaction_id,
            "event_type": "PaymentCompleted"
        }
    )
    db.add(outbox_message)
    
    db.commit()
    db.refresh(payment)
    
    return payment


def get_payment(db: Session, payment_id: int):
    """Get payment by ID"""
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_payments_by_order(db: Session, order_id: int):
    """Get payments for order"""
    return db.query(Payment).filter(Payment.order_id == order_id).all()


def process_outbox_messages(db: Session):
    """Process outbox messages"""
    unprocessed = db.query(OutboxMessage).filter(
        OutboxMessage.processed_on.is_(None)
    ).order_by(OutboxMessage.occurred_on).limit(10).all()
    
    for message in unprocessed:
        try:
            success = publish_message(
                exchange="flower_shop",
                routing_key=f"payment.{message.event_type.lower()}",
                message=message.payload
            )
            
            if success:
                message.processed_on = func.now()
                db.commit()
            else:
                message.error = "Failed to publish message"
                db.commit()
        except Exception as e:
            message.error = str(e)
            db.commit()

