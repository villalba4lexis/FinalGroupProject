from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

from ..schemas import guest_orders as guest_schemas
from ..controllers import orders as order_controller

from ..schemas import orders as order_schemas
from ..schemas.orders import OrderStatusUpdate, OrderTrackingOut

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

@router.post("/", response_model=schema.Order, status_code=status.HTTP_201_CREATED)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)



@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.post("/guest-orders", response_model=guest_schemas.GuestOrderOut, status_code=status.HTTP_201_CREATED)
def place_guest_order(order: guest_schemas.GuestOrderCreate, db: Session = Depends(get_db)):
    return order_controller.create_guest_order(order, db)

@router.post("/customer", response_model=order_schemas.CustomerOrderOut, status_code=status.HTTP_201_CREATED)
def place_customer_order(order: order_schemas.CustomerOrderCreate, db: Session = Depends(get_db)):
    return order_controller.create_customer_order(order, db)

@router.get("/tracking/{tracking_number}", response_model=OrderTrackingOut)
def get_order_status(tracking_number: str, db: Session = Depends(get_db)):
    return order_controller.get_order_status_by_tracking(tracking_number, db)

@router.put("/tracking/update", response_model=OrderTrackingOut)
def update_order_status(update: OrderStatusUpdate, db: Session = Depends(get_db)):
    return order_controller.update_order_status_by_tracking(update.tracking_number, update.status, db)
