"""API routes for Ordering Service"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas import OrderCreate, OrderResponse
from app.services import (
    create_order, get_order, get_user_orders,
    handle_payment_completed, handle_shipment_created, handle_shipment_delivered
)
from shared.database import get_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)
def create_order_endpoint(
    order: OrderCreate,
    user_id: int = 1,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Create new order"""
    return create_order(db, user_id, order)


@router.get("", response_model=List[OrderResponse])
def list_orders(
    user_id: int = 1,  # In real app, get from JWT token
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get user orders"""
    return get_user_orders(db, user_id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(
    order_id: int,
    user_id: int = 1,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Get order by ID"""
    order = get_order(db, order_id, user_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Internal endpoints for event handling (Saga)
@router.post("/{order_id}/payment-completed", status_code=200)
def payment_completed(order_id: int, db: Session = Depends(get_db)):
    """Handle payment completed event (internal)"""
    handle_payment_completed(db, order_id)
    return {"status": "ok"}


@router.post("/{order_id}/shipment-created", status_code=200)
def shipment_created(order_id: int, db: Session = Depends(get_db)):
    """Handle shipment created event (internal)"""
    handle_shipment_created(db, order_id)
    return {"status": "ok"}


@router.post("/{order_id}/shipment-delivered", status_code=200)
def shipment_delivered(order_id: int, db: Session = Depends(get_db)):
    """Handle shipment delivered event (internal)"""
    handle_shipment_delivered(db, order_id)
    return {"status": "ok"}

