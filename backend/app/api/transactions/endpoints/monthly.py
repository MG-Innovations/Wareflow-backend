from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import JWTBearer
from app.api.deps import get_db
from sqlalchemy.orm import Session
from app.core.api_response import ApiResponse
from app.core import security
from app.api.transactions.services.monthly import monthly
from app.api.payment.schemas.payment import PaymentGetResponse
from app.api.orders.schemas.order import OrderGet


router = APIRouter(prefix="/monthly")


@router.get("/transactions", dependencies=[Depends(JWTBearer())])
def get_monthly_transactions(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):

    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        tenant_id = payload.get("tenant_id")
        monthly_transactions = monthly.get_transactions(db, tenant_id)

        return ApiResponse.response_ok(
            data=[
                PaymentGetResponse.model_validate(payment).model_dump()
                for payment in monthly_transactions
            ]
        )

    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/orders", dependencies=[Depends(JWTBearer())])
def get_monthly_orders(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        tenant_id = payload.get("tenant_id")
        monthly_orders = monthly.get_orders(db, tenant_id)
        paid = [
            OrderGet.model_validate(order).model_dump()
            for order in monthly_orders
            if order.status == "Paid"
        ]
        unpaid = [
            OrderGet.model_validate(order).model_dump()
            for order in monthly_orders
            if order.status == "Unpaid"
        ]
        partial = [
            OrderGet.model_validate(order).model_dump()
            for order in monthly_orders
            if order.status == "Partially Paid"
        ]

        return ApiResponse.response_ok(data=[unpaid, partial, paid])

    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
