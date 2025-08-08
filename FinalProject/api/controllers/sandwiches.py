from sqlalchemy.orm import Session
from ..models import sandwiches as models
from ..schemas import sandwiches as schemas

def get_all_sandwiches(db: Session):
    return db.query(models.Sandwich).all()

def get_sandwich_by_id(sandwich_id: int, db: Session):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()

def create_sandwich(sandwich: schemas.SandwichCreate, db: Session):
    db_sandwich = models.Sandwich(**sandwich.model_dump())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichCreate, db: Session):
    db_sandwich = get_sandwich_by_id(sandwich_id, db)
    if not db_sandwich:
        return None
    for key, value in sandwich.model_dump().items():
        setattr(db_sandwich, key, value)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def delete_sandwich(sandwich_id: int, db: Session):
    db_sandwich = get_sandwich_by_id(sandwich_id, db)
    if not db_sandwich:
        return None
    db.delete(db_sandwich)
    db.commit()
    return db_sandwich