"""Business logic for Delivery Service"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Shipment, DeliveryStatus, OutboxMessage
from shared.rabbitmq_client import publish_message
import uuid
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def create_shipment(db: Session, order_id: int, user_id: int, delivery_address: str):
    """Create shipment for order"""
    shipment = Shipment(
        order_id=order_id,
        user_id=user_id,
        delivery_address=delivery_address,
        status=DeliveryStatus.PENDING,
        tracking_number=f"TRACK-{uuid.uuid4().hex[:8].upper()}"
    )
    db.add(shipment)
    db.flush()
    
    # Simulate shipping process
    shipment.status = DeliveryStatus.SHIPPED
    db.flush()
    
    # Create outbox message
    outbox_message = OutboxMessage(
        event_type="ShipmentCreated",
        payload={
            "shipment_id": shipment.id,
            "order_id": order_id,
            "tracking_number": shipment.tracking_number,
            "status": shipment.status.value,
            "event_type": "ShipmentCreated"
        }
    )
    db.add(outbox_message)
    
    db.commit()
    db.refresh(shipment)
    
    return shipment


def get_shipment(db: Session, shipment_id: int):
    """Get shipment by ID"""
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


def get_shipment_by_order(db: Session, order_id: int):
    """Get shipment by order ID"""
    return db.query(Shipment).filter(Shipment.order_id == order_id).first()


def update_shipment_status(db: Session, shipment_id: int, status: DeliveryStatus):
    """Update shipment status"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return None
    
    shipment.status = status
    db.commit()
    db.refresh(shipment)
    
    # If delivered, create event
    if status == DeliveryStatus.DELIVERED:
        outbox_message = OutboxMessage(
            event_type="ShipmentDelivered",
            payload={
                "shipment_id": shipment_id,
                "order_id": shipment.order_id,
                "event_type": "ShipmentDelivered"
            }
        )
        db.add(outbox_message)
        db.commit()
    
    return shipment


def process_outbox_messages(db: Session):
    """Process outbox messages"""
    unprocessed = db.query(OutboxMessage).filter(
        OutboxMessage.processed_on.is_(None)
    ).order_by(OutboxMessage.occurred_on).limit(10).all()
    
    for message in unprocessed:
        try:
            success = publish_message(
                exchange="flower_shop",
                routing_key=f"delivery.{message.event_type.lower()}",
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

