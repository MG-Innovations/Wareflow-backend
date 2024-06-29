from sqlalchemy.orm import Session
from uuid import UUID
from app.api.payment.db_models.payment import Payment
from app.api.orders.db_models.order import Order
from sqlalchemy import extract
import datetime
from typing import List


class MonthlyTransactions:
    def get_transactions(self, db: Session, id: UUID) -> List[Payment]:
        refreshed_monthly_transactions = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == id,
                extract("month", Payment.updated_at)
                == datetime.datetime.now().strftime("%m"),
            )
            .all()
        )
        return refreshed_monthly_transactions

    def get_orders(self, db: Session, id: UUID) -> List[Order]:
        refreshed_monthly_transactions = (
            db.query(Order)
            .filter(
                Order.tenant_id == id,
                extract("month", Order.created_at)
                == datetime.datetime.now().strftime("%m"),
            )
            .all()
        )
        return refreshed_monthly_transactions


monthly = MonthlyTransactions()
