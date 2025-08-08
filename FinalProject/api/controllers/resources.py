from sqlalchemy.orm import Session
from ..models import resources as models
from ..schemas import resources as schemas

def get_all_resources(db: Session):
    return db.query(models.Resource).all()

def get_resource_by_id(resource_id: int, db: Session):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def create_resource(resource: schemas.ResourceCreate, db: Session):
    db_resource = models.Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(resource_id: int, resource: schemas.ResourceCreate, db: Session):
    db_resource = get_resource_by_id(resource_id, db)
    if not db_resource:
        return None
    for key, value in resource.model_dump().items():
        setattr(db_resource, key, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def delete_resource(resource_id: int, db: Session):
    db_resource = get_resource_by_id(resource_id, db)
    if not db_resource:
        return None
    db.delete(db_resource)
    db.commit()
    return db_resource
