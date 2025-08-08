from pydantic import BaseModel, ConfigDict
from typing import Optional

class ReviewBase(BaseModel):
    sandwich_id: int
    user_id: Optional[int] = None
    rating: float
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)