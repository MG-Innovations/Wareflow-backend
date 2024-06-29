from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.api.payment.db_models.payment import Payment
from app.api.orders.db_models.order import Order
from sqlalchemy import and_
import datetime


class WeeklyTransactions:
    def get_transactions(self, db: Session, id: UUID) -> List[Payment]:
        today = datetime.date.today()

        # Calculate the start of the week (Monday)
        start_of_week = today - datetime.timedelta(days=today.weekday())

        # Calculate the end of the week (Sunday)
        end_of_week = start_of_week + datetime.timedelta(days=6)
        refreshed_monthly_transactions = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == id,
                and_(
                    Payment.updated_at >= start_of_week,
                    Payment.updated_at <= end_of_week,
                ),
            )
            .all()
        )
        return refreshed_monthly_transactions

    def get_orders(self, db: Session, id: UUID) -> List[Order]:
        today = datetime.date.today()

        # Calculate the start of the week (Monday)
        start_of_week = today - datetime.timedelta(days=today.weekday())

        # Calculate the end of the week (Sunday)
        end_of_week = start_of_week + datetime.timedelta(days=7)
        weekly_orders = (
            db.query(Order)
            .filter(
                Order.tenant_id == id,
                and_(
                    Order.created_at >= start_of_week,
                    Order.created_at <= end_of_week,
                ),
            )
            .all()
        )
        return weekly_orders


weekly = WeeklyTransactions()
