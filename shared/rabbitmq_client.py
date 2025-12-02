"""RabbitMQ client for message bus"""
import pika
import json
import os
from typing import Callable, Optional

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")


def get_connection():
    """Get RabbitMQ connection"""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)


def publish_message(exchange: str, routing_key: str, message: dict):
    """Publish message to RabbitMQ"""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
        
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        connection.close()
        return True
    except Exception as e:
        print(f"RabbitMQ publish error: {e}")
        return False


def consume_messages(queue: str, callback: Callable, exchange: Optional[str] = None, routing_key: Optional[str] = None):
    """Consume messages from RabbitMQ"""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        if exchange:
            channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
        
        channel.queue_declare(queue=queue, durable=True)
        
        if exchange and routing_key:
            channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        
        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Message processing error: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        channel.basic_consume(queue=queue, on_message_callback=on_message)
        channel.start_consuming()
    except Exception as e:
        print(f"RabbitMQ consume error: {e}")

