from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from ..schemas import sandwiches as schemas
from ..controllers import sandwiches as controllers
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/sandwiches",
    tags=["Sandwiches"]
)


@router.get("/", response_model=List[schemas.Sandwich])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return controllers.get_all_sandwiches(db)


@router.get("/{sandwich_id}", response_model=schemas.Sandwich)
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = controllers.get_sandwich_by_id(sandwich_id, db)
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich


@router.post("/", response_model=schemas.Sandwich, status_code=status.HTTP_201_CREATED)
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return controllers.create_sandwich(sandwich, db)


@router.put("/{sandwich_id}", response_model=schemas.Sandwich)
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    updated = controllers.update_sandwich(sandwich_id, sandwich, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return updated


@router.delete("/{sandwich_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    deleted = controllers.delete_sandwich(sandwich_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return

def load_routes(app):
    app.include_router(router)

