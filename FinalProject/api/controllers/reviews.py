from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import reviews as model
from ..schemas import reviews as schema
from sqlalchemy.exc import SQLAlchemyError

def create_review(db: Session, review: schema.ReviewCreate):
    new_review = model.Review(**review.model_dump())
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_reviews_by_sandwich(db: Session, sandwich_id: int):
    try:
        return db.query(model.Review).filter(model.Review.sandwich_id == sandwich_id).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)