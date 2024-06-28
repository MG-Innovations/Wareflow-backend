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
        db.commit()
        db.refresh(db_payment)
        return db_payment

    def get_payment_by_id(self, db: Session, payment_id: UUID) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payments(self, db: Session) -> List[Payment]:
        return db.query(Payment).all()

    def get_all_payment_by_tenant_id(
        self, db: Session, tenant_id: UUID
    ) -> List[Payment]:
        return db.query(Payment).filter(Payment.tenant_id == tenant_id).all()

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
