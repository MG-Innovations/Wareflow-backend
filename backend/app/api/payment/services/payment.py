from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.payment.db_models.payment import Payment
from app.api.payment.schemas.payment import (
    Payment as BaseProduct,
    PaymentDelete,
    PaymentGet,
    PaymentGetResponse,
    PaymentUpdate,
)
from app.api.orders.services.order import OrderService
from app.core.enums import PaymentStatus
from app.api.orders.db_models.customer import Customer
from app.api.orders.db_models.order import Order


class PaymentService:

    def create_payment(
        self, db: Session, payment: BaseProduct, user_id: UUID, tenant_id: UUID
    ) -> Payment:
        db_payment = Payment(
            **payment.model_dump(),
            tenant_id=tenant_id,
            user_id=user_id,
            created_by=user_id,
            updated_by=user_id
        )
        db.add(db_payment)
        
        # Use the OrderService instance to retrieve and update the order
        order_service = OrderService()
        order = order_service.get(db, payment.order_id)
        print(order)
        if order:
            
            order.amount_received += db_payment.amount_paid
            if order.amount_received < order.order_value:
                order.status = PaymentStatus.Partially_paid
            else:
                order.status = PaymentStatus.Paid
            db.add(order)

        db.commit()
        db.refresh(db_payment)
        return db_payment

    def get_payment_by_id(self, db: Session, payment_id: UUID) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payments(self, db: Session,query:str) -> List[Payment]:
        return db.query(Payment).all()

    def get_all_payment_by_tenant_id(
        self, db: Session, tenant_id: UUID,query:str,start_date:str,end_date:str
    ) -> List[Payment]:
        filters = [Payment.tenant_id == tenant_id]
        if query:
            query_customers = db.query(Customer).where(Customer.tenant_id == tenant_id,Customer.name.like(f"%{query}%")).all()
            customer_ids = [str(customer.id) for customer in query_customers]
            query_orders = db.query(Order).where(Order.tenant_id == tenant_id,Order.customer_id.in_(customer_ids)).all()
            order_ids = [str(order.id) for order in query_orders]
            filters.append(Payment.order_id.in_(order_ids))
        if(start_date and end_date):
            filters.append(Payment.created_at.between(start_date, end_date))    
        return db.query(Payment).filter(*filters).limit(40).all()
    
    
    def get_all_payment_by_order_id(
        self, db: Session, order_id: UUID, tenant_id: UUID
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id, Payment.tenant_id == tenant_id)
            .all()
        )

    def delete_payment(self, db: Session, payment_id: UUID) -> bool:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            db.delete(payment)
            db.commit()
            return True
        return False


payment_service = PaymentService()
