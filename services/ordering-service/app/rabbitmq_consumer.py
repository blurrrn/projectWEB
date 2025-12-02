"""RabbitMQ consumer for Saga events"""
from shared.rabbitmq_client import consume_messages
from app.event_handlers import (
    handle_payment_completed_event,
    handle_shipment_created_event,
    handle_shipment_delivered_event
)
import threading
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def start_rabbitmq_consumer():
    """Start RabbitMQ consumer in background thread"""
    def consume_payment():
        try:
            consume_messages(
                queue="ordering_payment_events",
                callback=lambda msg: handle_payment_completed_event(msg),
                exchange="flower_shop",
                routing_key="payment.paymentcompleted"
            )
        except Exception as e:
            print(f"RabbitMQ payment consumer error: {e}")
    
    def consume_delivery():
        try:
            consume_messages(
                queue="ordering_delivery_events",
                callback=lambda msg: handle_event(msg),
                exchange="flower_shop",
                routing_key="delivery.*"
            )
        except Exception as e:
            print(f"RabbitMQ delivery consumer error: {e}")
    
    thread1 = threading.Thread(target=consume_payment, daemon=True)
    thread1.start()
    
    thread2 = threading.Thread(target=consume_delivery, daemon=True)
    thread2.start()


def handle_event(message: dict):
    """Route event to appropriate handler"""
    event_type = message.get("event_type") or message.get("type")
    
    if event_type == "ShipmentCreated":
        handle_shipment_created_event(message)
    elif event_type == "ShipmentDelivered":
        handle_shipment_delivered_event(message)

