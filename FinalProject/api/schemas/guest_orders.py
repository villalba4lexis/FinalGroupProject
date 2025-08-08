from pydantic import BaseModel, Field
from typing import List
from .orders import OrderDetailOut


class GuestOrderItem(BaseModel):
    sandwich_id: int
    quantity: int = Field(..., gt=0)


class GuestOrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    customer_email: str
    description: str
    items: List[GuestOrderItem]


class GuestOrderOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    customer_address: str
    customer_email: str
    description: str
    total_price: float
    status: str
    tracking_number: str
    order_details: List[OrderDetailOut]

    class Config:
        from_attributes = True
