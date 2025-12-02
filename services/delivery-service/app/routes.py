"""API routes for Delivery Service"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ShipmentResponse
from app.services import (
    create_shipment, get_shipment, get_shipment_by_order,
    update_shipment_status
)
from app.models import DeliveryStatus
from shared.database import get_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

router = APIRouter(prefix="/delivery", tags=["delivery"])


@router.post("/create", response_model=ShipmentResponse, status_code=201)
def create_shipment_endpoint(
    order_id: int,
    user_id: int,
    delivery_address: str,
    db: Session = Depends(get_db)
):
    """Create shipment for order"""
    return create_shipment(db, order_id, user_id, delivery_address)


@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment_endpoint(shipment_id: int, db: Session = Depends(get_db)):
    """Get shipment by ID"""
    shipment = get_shipment(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.get("/order/{order_id}", response_model=ShipmentResponse)
def get_order_shipment(order_id: int, db: Session = Depends(get_db)):
    """Get shipment by order ID"""
    shipment = get_shipment_by_order(db, order_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.post("/{shipment_id}/deliver", response_model=ShipmentResponse)
def mark_delivered(shipment_id: int, db: Session = Depends(get_db)):
    """Mark shipment as delivered"""
    shipment = update_shipment_status(db, shipment_id, DeliveryStatus.DELIVERED)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

