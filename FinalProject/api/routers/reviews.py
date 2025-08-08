from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import reviews as schema
from ..controllers import reviews as controller

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schema.ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(review: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create_review(db, review)

@router.get("/sandwich/{sandwich_id}", response_model=list[schema.ReviewOut])
def get_reviews_for_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.read_reviews_by_sandwich(db, sandwich_id)
