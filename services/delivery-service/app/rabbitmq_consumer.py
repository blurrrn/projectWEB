"""RabbitMQ consumer for Delivery Service"""
from shared.rabbitmq_client import consume_messages
from app.event_handlers import handle_order_paid
import threading
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def start_rabbitmq_consumer():
    """Start RabbitMQ consumer in background thread"""
    def consume():
        try:
            consume_messages(
                queue="delivery_order_events",
                callback=handle_order_paid,
                exchange="flower_shop",
                routing_key="order.orderpaid"
            )
        except Exception as e:
            print(f"RabbitMQ consumer error: {e}")
    
    thread = threading.Thread(target=consume, daemon=True)
    thread.start()

