from sqlalchemy.orm import Session
from ..models import recipes as models
from ..schemas import recipes as schemas

def get_all_recipes(db: Session):
    return db.query(models.Recipe).all()

def get_recipe_by_id(recipe_id: int, db: Session):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def create_recipe(recipe: schemas.RecipeCreate, db: Session):
    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: Session):
    db_recipe = get_recipe_by_id(recipe_id, db)
    if not db_recipe:
        return None
    for key, value in recipe.model_dump().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(recipe_id: int, db: Session):
    db_recipe = get_recipe_by_id(recipe_id, db)
    if not db_recipe:
        return None
    db.delete(db_recipe)
    db.commit()
    return db_recipe
