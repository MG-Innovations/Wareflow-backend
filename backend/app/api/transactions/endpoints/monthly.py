from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import JWTBearer
from app.api.deps import get_db
from sqlalchemy import extract
from sqlalchemy.orm import Session
import datetime
from app.api.payment.db_models.payment import Payment
from app.core.api_response import ApiResponse
from app.core import security

router = APIRouter(prefix="/transactions")


@router.get("/monthly", dependencies=[Depends(JWTBearer())])
def get_weekly_transactions(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):

    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
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

        return ApiResponse.response_ok(data=refreshed_monthly_transactions)

    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
