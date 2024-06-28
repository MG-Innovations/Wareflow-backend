from uuid import UUID
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union
from app.api.orders.db_models.order import Order
from app.api.orders.db_models.order_item import OrderItem
from app.api.orders.schemas.order import OrderCreateInDb, OrderItemCreate
from app.api.product.services.product import product_service
from core import security

class OrderService:

    def get(self, db: Session, order_id: UUID) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()
    
    def get_all(self, db: Session, tenant_id:UUID,skip:int = 0, limit:int=10) -> List[Order]:
        return db.query(Order).filter_by(tenant_id=tenant_id).offset(skip).limit(limit).all()

    def create_order_with_items(self, db: Session, schema: OrderCreateInDb, items: List[OrderItemCreate]) -> Optional[Order]:
        # Create the Order instance
        for item_schema in items:
            product = product_service.get_product_by_id(db, item_schema.product_id)
            if not product or product.stock < item_schema.quantity:
                raise ValueError(f"Insufficient stock for product ID: {item_schema.product_id}")

        order = Order(
            tenant_id=schema.tenant_id,
            order_value=schema.order_value,
            customer_id=schema.customer_id,
            created_by=schema.created_by,
            updated_by=schema.updated_by
        )

        # Create OrderItem instances and add them to the order
        for item_schema in items:
            product = product_service.get_product_by_id(db, item_schema.product_id)
            order_item = OrderItem(
                product_id=item_schema.product_id,
                order_id = order.id,
                quantity=item_schema.quantity,
                price=item_schema.price,
                tenant_id=schema.tenant_id
            )
            order.order_items.append(order_item)
            product.stock -= item_schema.quantity
            db.add(product)
        # Add the order to the session and commit
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
order = OrderService()    
