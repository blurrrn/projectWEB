"""Background tasks for Payment Service"""
import asyncio
from sqlalchemy.orm import Session
from app.services import process_outbox_messages
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


async def process_outbox_worker():
    """Background worker to process outbox messages"""
    while True:
        try:
            db = SessionLocal()
            try:
                process_outbox_messages(db)
            finally:
                db.close()
        except Exception as e:
            print(f"Outbox processing error: {e}")
        
        await asyncio.sleep(5)


async def start_background_tasks():
    """Start all background tasks"""
    asyncio.create_task(process_outbox_worker())

