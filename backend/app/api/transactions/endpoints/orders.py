from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import JWTBearer
from app.api.deps import get_db
from sqlalchemy.orm import Session
from app.core.api_response import ApiResponse
from app.api.transactions.services.orders import OrdersService

router = APIRouter(prefix="/orders")


@router.get("/weekly", dependencies=[Depends(JWTBearer())])
def get_weekly_orders(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token
        order_service = OrdersService()
        refreshed_weekly_orders = order_service.get_weekly_orders(db, token)
        return ApiResponse.response_ok(data=refreshed_weekly_orders)
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/monthly", dependencies=[Depends(JWTBearer())])
def get_monthly_orders(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token
        order_service = OrdersService()
        refreshed_monthly_orders = order_service.get_monthly_orders(db, token)
        return ApiResponse.response_ok(data=refreshed_monthly_orders)
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
