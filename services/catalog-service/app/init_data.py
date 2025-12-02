"""Initialize test data"""
from sqlalchemy.orm import Session
from app.models import Flower, FlowerType, Category, Bouquet
from shared.database import SessionLocal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


def init_test_data():
    """Create test flowers and categories"""
    db = SessionLocal()
    try:
        # Create categories
        romantic = db.query(Category).filter(Category.name == "Romantic").first()
        if not romantic:
            romantic = Category(name="Romantic", description="Romantic bouquets")
            db.add(romantic)
        
        birthday = db.query(Category).filter(Category.name == "Birthday").first()
        if not birthday:
            birthday = Category(name="Birthday", description="Birthday bouquets")
            db.add(birthday)
        
        db.flush()
        
        # Create flowers
        flowers_data = [
            {"name": "Red Rose", "description": "Beautiful red rose", "price": 150.0, "stock_quantity": 100, "flower_type": FlowerType.ROSE},
            {"name": "White Rose", "description": "Elegant white rose", "price": 140.0, "stock_quantity": 80, "flower_type": FlowerType.ROSE},
            {"name": "Pink Tulip", "description": "Charming pink tulip", "price": 120.0, "stock_quantity": 90, "flower_type": FlowerType.TULIP},
            {"name": "White Lily", "description": "Pure white lily", "price": 130.0, "stock_quantity": 70, "flower_type": FlowerType.LILY},
            {"name": "Purple Orchid", "description": "Exotic purple orchid", "price": 200.0, "stock_quantity": 50, "flower_type": FlowerType.ORCHID},
        ]
        
        for flower_data in flowers_data:
            existing = db.query(Flower).filter(Flower.name == flower_data["name"]).first()
            if not existing:
                flower = Flower(**flower_data)
                db.add(flower)
        
        # Create bouquets
        romantic_bouquet = db.query(Bouquet).filter(Bouquet.name == "Romantic Bouquet").first()
        if not romantic_bouquet:
            romantic_bouquet = Bouquet(
                name="Romantic Bouquet",
                description="A beautiful romantic bouquet with red roses",
                price=500.0,
                stock_quantity=30,
                category_id=romantic.id
            )
            db.add(romantic_bouquet)
        
        birthday_bouquet = db.query(Bouquet).filter(Bouquet.name == "Birthday Bouquet").first()
        if not birthday_bouquet:
            birthday_bouquet = Bouquet(
                name="Birthday Bouquet",
                description="Colorful birthday bouquet",
                price=450.0,
                stock_quantity=25,
                category_id=birthday.id
            )
            db.add(birthday_bouquet)
        
        db.commit()
        print("Test catalog data created successfully")
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_test_data()

