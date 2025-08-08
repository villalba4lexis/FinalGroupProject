from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .order_details import OrderDetail

class OrderBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    customer_email: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None

class OrderDetailOut(BaseModel):
    sandwich_id: int
    amount: int

    class Config:
        from_attributes = True

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetailOut] = []

    class ConfigDict:
        from_attributes = True

class CustomerOrderItem(BaseModel):
    sandwich_id: int
    quantity: int


class CustomerOrderCreate(BaseModel):
    user_id: int
    order_type: str  # "pickup" or "delivery"
    description: str
    items: List[CustomerOrderItem]


class CustomerOrderOut(BaseModel):
    id: int
    user_id: int
    order_type: str
    total_price: float
    status: str
    tracking_number: str

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    tracking_number: str
    status: str

class OrderTrackingOut(BaseModel):
    id: int
    tracking_number: str
    status: str

    model_config = ConfigDict(from_attributes=True)

