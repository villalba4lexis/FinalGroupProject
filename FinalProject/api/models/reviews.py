from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    user_id = Column(Integer)  # assuming no users table yet, or nullable
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)

    sandwich = relationship("Sandwich", back_populates="reviews")