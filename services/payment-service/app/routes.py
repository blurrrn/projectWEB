"""API routes for Payment Service"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import PaymentResponse
from app.services import process_payment, get_payment, get_payments_by_order
from shared.database import get_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/process", response_model=PaymentResponse, status_code=201)
def process_payment_endpoint(
    order_id: int,
    user_id: int,
    amount: float,
    db: Session = Depends(get_db)
):
    """Process payment for order"""
    return process_payment(db, order_id, user_id, amount)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_endpoint(payment_id: int, db: Session = Depends(get_db)):
    """Get payment by ID"""
    payment = get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/order/{order_id}", response_model=list[PaymentResponse])
def get_order_payments(order_id: int, db: Session = Depends(get_db)):
    """Get payments for order"""
    return get_payments_by_order(db, order_id)

