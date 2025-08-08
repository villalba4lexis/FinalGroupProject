from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class GuestOrder(Base):
    __tablename__ = "guest_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    customer_phone = Column(String(20))
    customer_address = Column(String(200))
    customer_email = Column(String(200))
    total_price = Column(Float)
    description = Column(String(300))
    status = Column(String(50))
    tracking_number = Column(String(50), unique=True)

    order_details = relationship("OrderDetail", back_populates="guest_order")
