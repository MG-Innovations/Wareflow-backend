import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List, Optional
from app.api.payment.db_models.payment import Payment
from app.core import security


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

        refreshed_weekly_transactions = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == tenant_id,
                Payment.created_at >= start_of_week,
                Payment.created_at <= end_of_week,
            )
            .all()
        )

        return refreshed_weekly_transactions

    def get_monthly_transactions(self, db: Session, token: str) -> List[Payment]:
        payload = security.decode_access_token(token)
        tenant_id = payload.get("tenant_id")

        refreshed_monthly_transactions = (
            db.query(Payment)
            .filter(
                Payment.tenant_id == tenant_id,
                extract("month", Payment.updated_at)
                == datetime.datetime.now().strftime("%m"),
            )
            .all()
        )

        return refreshed_monthly_transactions
