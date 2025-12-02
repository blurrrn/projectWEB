"""Business logic for Ordering Service"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models import Order, OrderItem, OrderStatus, OutboxMessage
from app.schemas import OrderCreate
from shared.rabbitmq_client import publish_message
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def create_order(db: Session, user_id: int, order_data: OrderCreate):
    """Create new order with Transaction Outbox"""
    # Calculate total (simplified - in real app would fetch prices from catalog service)
    total_amount = sum(item.quantity * 100.0 for item in order_data.items)  # Placeholder price
    
    # Create order
    order = Order(
        user_id=user_id,
        status=OrderStatus.CREATED,
        total_amount=total_amount,
        delivery_address=order_data.delivery_address
    )
    db.add(order)
    db.flush()  # Get order.id
    
    # Create order items
    for item in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            flower_id=item.flower_id,
            quantity=item.quantity,
            price=100.0  # Placeholder
        )
        db.add(order_item)
    
    # Create outbox message (Transaction Outbox pattern)
    outbox_message = OutboxMessage(
        event_type="OrderCreated",
        payload={
            "order_id": order.id,
            "user_id": user_id,
            "total_amount": float(total_amount),
            "items": [{"flower_id": item.flower_id, "quantity": item.quantity} for item in order_data.items],
            "delivery_address": order_data.delivery_address,
            "event_type": "OrderCreated"
        }
    )
    db.add(outbox_message)
    
    # Commit transaction
    db.commit()
    db.refresh(order)
    
    return order


def get_order(db: Session, order_id: int, user_id: int = None):
    """Get order by ID"""
    query = db.query(Order).filter(Order.id == order_id)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.first()


def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get user orders"""
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: OrderStatus):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order


def process_outbox_messages(db: Session):
    """Process outbox messages (should run in background worker)"""
    unprocessed = db.query(OutboxMessage).filter(
        OutboxMessage.processed_on.is_(None)
    ).order_by(OutboxMessage.occurred_on).limit(10).all()
    
    for message in unprocessed:
        try:
            # Publish to RabbitMQ
            success = publish_message(
                exchange="flower_shop",
                routing_key=f"order.{message.event_type.lower()}",
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


def handle_payment_completed(db: Session, order_id: int):
    """Handle payment completed event"""
    order = update_order_status(db, order_id, OrderStatus.PAYMENT_COMPLETED)
    
    if order:
        # Create outbox message for shipping
        outbox_message = OutboxMessage(
            event_type="OrderPaid",
            payload={
                "order_id": order_id,
                "user_id": order.user_id,
                "delivery_address": order.delivery_address,
                "event_type": "OrderPaid"
            }
        )
        db.add(outbox_message)
        db.commit()


def handle_shipment_created(db: Session, order_id: int):
    """Handle shipment created event"""
    order = update_order_status(db, order_id, OrderStatus.SHIPPING)
    return order


def handle_shipment_delivered(db: Session, order_id: int):
    """Handle shipment delivered event"""
    order = update_order_status(db, order_id, OrderStatus.COMPLETED)
    return order

