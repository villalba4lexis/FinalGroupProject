from . import users, orders, sandwiches, reviews, resources, recipes, order_details
from ..dependencies.database import engine, Base

def index():
    Base.metadata.create_all(engine)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)