"""API Gateway - Single entry point for all services"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os

SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
    "catalog": os.getenv("CATALOG_SERVICE_URL", "http://catalog-service:8002"),
    "ordering": os.getenv("ORDERING_SERVICE_URL", "http://ordering-service:8003"),
    "payment": os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:8004"),
    "delivery": os.getenv("DELIVERY_SERVICE_URL", "http://delivery-service:8005"),
}

app = FastAPI(
    title="Flower Shop API Gateway",
    description="Single entry point for all microservices",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def proxy_middleware(request: Request, call_next):
    """Proxy requests to appropriate services"""
    path = request.url.path
    
    # Health check
    if path == "/health":
        return await call_next(request)
    
    # Route to services
    if path.startswith("/api/auth"):
        target_url = SERVICES["auth"] + path.replace("/api/auth", "")
    elif path.startswith("/api/catalog") or path.startswith("/api/flowers") or path.startswith("/api/bouquets"):
        target_url = SERVICES["catalog"] + path.replace("/api/catalog", "").replace("/api", "")
    elif path.startswith("/api/orders"):
        target_url = SERVICES["ordering"] + path.replace("/api/orders", "")
    elif path.startswith("/api/payments"):
        target_url = SERVICES["payment"] + path.replace("/api/payments", "")
    elif path.startswith("/api/delivery"):
        target_url = SERVICES["delivery"] + path.replace("/api/delivery", "")
    else:
        return await call_next(request)
    
    # Proxy request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=dict(request.headers),
                params=dict(request.query_params),
                content=await request.body(),
                timeout=30.0
            )
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Flower Shop API Gateway",
        "services": {
            "auth": "/api/auth",
            "catalog": "/api/catalog",
            "orders": "/api/orders",
            "payments": "/api/payments",
            "delivery": "/api/delivery"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

