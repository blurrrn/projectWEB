"""API routes for Catalog Service"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import (
    FlowerCreate, FlowerUpdate, FlowerResponse,
    CategoryCreate, CategoryResponse,
    BouquetCreate, BouquetResponse
)
from app.services import (
    get_flower, get_flowers, create_flower, update_flower,
    get_categories, create_category,
    get_bouquets, get_bouquet, create_bouquet
)
from shared.database import get_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

router = APIRouter(prefix="/catalog", tags=["catalog"])


# Flower endpoints
@router.get("/flowers", response_model=List[FlowerResponse])
def list_flowers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of flowers"""
    flowers = get_flowers(db, skip=skip, limit=limit, search=search)
    return flowers


@router.get("/flowers/{flower_id}", response_model=FlowerResponse)
def get_flower_by_id(flower_id: int, db: Session = Depends(get_db)):
    """Get flower by ID"""
    flower = get_flower(db, flower_id)
    if not flower:
        raise HTTPException(status_code=404, detail="Flower not found")
    return flower


@router.post("/flowers", response_model=FlowerResponse, status_code=201)
def create_flower_endpoint(flower: FlowerCreate, db: Session = Depends(get_db)):
    """Create new flower"""
    return create_flower(db, flower)


@router.put("/flowers/{flower_id}", response_model=FlowerResponse)
def update_flower_endpoint(
    flower_id: int,
    flower: FlowerUpdate,
    db: Session = Depends(get_db)
):
    """Update flower"""
    updated = update_flower(db, flower_id, flower)
    if not updated:
        raise HTTPException(status_code=404, detail="Flower not found")
    return updated


# Category endpoints
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of categories"""
    return get_categories(db, skip=skip, limit=limit)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create new category"""
    return create_category(db, category)


# Bouquet endpoints
@router.get("/bouquets", response_model=List[BouquetResponse])
def list_bouquets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of bouquets"""
    return get_bouquets(db, skip=skip, limit=limit)


@router.get("/bouquets/{bouquet_id}", response_model=BouquetResponse)
def get_bouquet_by_id(bouquet_id: int, db: Session = Depends(get_db)):
    """Get bouquet by ID"""
    bouquet = get_bouquet(db, bouquet_id)
    if not bouquet:
        raise HTTPException(status_code=404, detail="Bouquet not found")
    return bouquet


@router.post("/bouquets", response_model=BouquetResponse, status_code=201)
def create_bouquet_endpoint(bouquet: BouquetCreate, db: Session = Depends(get_db)):
    """Create new bouquet"""
    return create_bouquet(db, bouquet)

