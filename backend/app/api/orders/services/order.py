from uuid import UUID
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union
from app.api.orders.db_models.order import Order
from app.api.orders.db_models.order_item import OrderItem
from app.api.orders.schemas.order import OrderCreateInDb, OrderItemCreate
from app.api.product.services.product import product_service
from app.api.orders.db_models.customer import Customer
from datetime import datetime
from core.enums import PaymentStatus

class OrderService:

    def get(self, db: Session, order_id: UUID) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()
    
    def get_all(self, 
            db: Session, 
            tenant_id: UUID, 
            start_date: str, 
            end_date: str, 
            query: str = None) -> List[Order]:
        
        filters = [Order.tenant_id == tenant_id]
        if query:
            query_customers = db.query(Customer).filter(Customer.name.ilike(f"%{query}%")).all()
            customer_ids =[str(customer.id) for customer in query_customers]
            if customer_ids:
                filters.append(Order.customer_id.in_(customer_ids))
        
        
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
            end_date_obj = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
            filters.append(Order.created_at.between(start_date_obj, end_date_obj))
        
        orders = (
            db.query(Order)
            .filter(*filters)
            .limit(40)
            .all()
        )

        return orders
    
    def get_unpaid_orders(self, db: Session, tenant_id: UUID) -> List[Order]:
        return db.query(Order).filter(
            Order.tenant_id == tenant_id,
            Order.status.in_([PaymentStatus.Unpaid, PaymentStatus.Partially_paid])
        ).all()

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
