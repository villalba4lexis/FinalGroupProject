import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal


from ..schemas import guest_orders, orders
from ..models import sandwiches as sandwich_model
from ..models import orders as order_model
from ..models import order_details as detail_model

def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def create_guest_order(order: guest_orders.GuestOrderCreate, db: Session):
    total_price = Decimal("0.0")

    for item in order.items:
        sandwich = db.query(sandwich_model.Sandwich).filter(
            sandwich_model.Sandwich.id == item.sandwich_id
        ).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail=f"Sandwich ID {item.sandwich_id} not found")

        total_price += Decimal(str(sandwich.price)) * item.quantity

    tracking_number = str(uuid.uuid4())[:8]

    db_order = order_model.Order(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        customer_email=order.customer_email,
        description=order.description,
        total_price=total_price,
        status="Pending",
        tracking_number=tracking_number
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_detail = detail_model.OrderDetail(
            order_id=db_order.id,
            sandwich_id=item.sandwich_id,
            amount=item.quantity
        )
        db.add(db_detail)

    db.commit()
    return db_order

def create_customer_order(order: orders.CustomerOrderCreate, db: Session):
    total_price = Decimal("0.0")

    for item in order.items:
        sandwich = db.query(sandwich_model.Sandwich).filter(
            sandwich_model.Sandwich.id == item.sandwich_id
        ).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail=f"Sandwich ID {item.sandwich_id} not found")

        total_price += Decimal(str(sandwich.price)) * item.quantity

    tracking_number = str(uuid.uuid4())[:8]

    db_order = order_model.Order(
        user_id=order.user_id,
        order_type=order.order_type,
        description=order.description,
        total_price=total_price,
        status="Pending",
        tracking_number=tracking_number
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_detail = detail_model.OrderDetail(
            order_id=db_order.id,
            sandwich_id=item.sandwich_id,
            amount=item.quantity
        )
        db.add(db_detail)

    db.commit()
    return db_order

def update_order_status_by_tracking(tracking_number: str, new_status: str, db: Session):
    order = db.query(order_model.Order).filter(order_model.Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Tracking number not found")

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def get_order_status_by_tracking(tracking_number: str, db: Session):
    order = db.query(order_model.Order).filter(order_model.Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Tracking number not found")
    return order