"""Main FastAPI application for Payment Service"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.background_tasks import start_background_tasks
from app.rabbitmq_consumer import start_rabbitmq_consumer
from shared.database import engine, Base
import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Service",
    description="Payment Processing Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    await start_background_tasks()
    start_rabbitmq_consumer()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "payment-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

