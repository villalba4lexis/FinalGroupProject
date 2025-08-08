from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from ..schemas import resources as schemas
from ..controllers import resources as controllers
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.get("/", response_model=List[schemas.Resource])
def read_all_resources(db: Session = Depends(get_db)):
    return controllers.get_all_resources(db)


@router.get("/{resource_id}", response_model=schemas.Resource)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = controllers.get_resource_by_id(resource_id, db)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource


@router.post("/", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return controllers.create_resource(resource, db)


@router.put("/{resource_id}", response_model=schemas.Resource)
def update_resource(resource_id: int, resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    updated = controllers.update_resource(resource_id, resource, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return updated


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    deleted = controllers.delete_resource(resource_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return

def load_routes(app):
    app.include_router(router)