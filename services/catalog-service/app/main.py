"""Main FastAPI application for Catalog Service"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.init_data import init_test_data
from shared.database import engine, Base
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize test data
init_test_data()

app = FastAPI(
    title="Catalog Service",
    description="Flower and Bouquet Catalog Service",
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


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "catalog-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

