from sqlalchemy import Column, ForeignKey, Integer, String,Float, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)
    calories = Column(Float, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    category = Column(String(100), nullable=True)

    recipes = relationship("Recipe", back_populates="sandwich")
    order_details = relationship("OrderDetail", back_populates="sandwich")
    reviews = relationship("Review", back_populates="sandwich", cascade="all, delete")

