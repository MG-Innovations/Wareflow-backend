import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List, Optional
from app.api.orders.db_models.order import Order
from app.core import security


class OrdersService:
    def get_monthly_orders(self, db: Session, token: str) -> List[Order]:
        payload = security.decode_access_token(token)
        tenant_id = payload.get("tenant_id")

        refreshed_monthly_transactions = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id,
                extract("month", Order.created_at)
                == datetime.datetime.now().strftime("%m"),
            )
            .all()
        )

        return refreshed_monthly_transactions

    def get_weekly_orders(self, db: Session, token: str) -> List[Order]:
        payload = security.decode_access_token(token)
        today = datetime.date.today()

        # Calculate the start of the week (Monday)
        start_of_week = today - datetime.timedelta(days=today.weekday())

        # Calculate the end of the week (Sunday)
        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Extract the UUID of the tenant
        tenant_id = payload.get("tenant_id")

        refreshed_weekly_transactions = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id,
                Order.created_at >= start_of_week,
                Order.created_at <= end_of_week,
            )
            .all()
        )

        return refreshed_weekly_transactions
