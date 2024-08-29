import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List, Optional
from app.api.payment.db_models.payment import Payment
from app.core import security
from app.api.orders.db_models.customer import Customer
from app.api.orders.db_models.order import Order
from sqlalchemy import and_, select


class TransactionsService:
    def get_weekly_transactions(self, db: Session, token: str) -> List[Payment]:
        payload = security.decode_access_token(token)
        today = datetime.date.today()

        # Calculate the start of the week (Monday)
        start_of_week = today - datetime.timedelta(days=today.weekday())

        # Calculate the end of the week (Sunday)
        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Extract the UUID of the tenant
        tenant_id = payload.get("tenant_id")
        stmt = (
            select(
                Payment.id,
                Payment.amount_paid,
                Payment.payment_type,
                Payment.tenant_id,
                Payment.order_id,
                Payment.user_id,
                Customer.name.label("customer_name"),
                Payment.description,
            )
            .select_from(Payment)
            .join(Order, Order.id == Payment.order_id)
            .join(Customer, Customer.id == Order.customer_id)
            .filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.created_at >= start_of_week,
                    Payment.created_at <= end_of_week,
                )
            )
        )
        results = db.execute(stmt)
        transactions = []
        for row in results:
            data = {
                "id": row.id,
                "amount_paid": row.amount_paid,
                "payment_type": row.payment_type,
                "tenant_id": row.tenant_id,
                "order_id": row.order_id,
                "customer_name": row.customer_name,
                "description": row.description,
            }
            transactions.append(data)

        return transactions

    def get_monthly_transactions(self, db: Session, token: str) -> List[Payment]:
        payload = security.decode_access_token(token)
        tenant_id = payload.get("tenant_id")

        refreshed_monthly_transactions = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == tenant_id,
                extract("month", Payment.created_at)
                == datetime.datetime.now().strftime("%m"),
            )
            .all()
        )

        return refreshed_monthly_transactions
