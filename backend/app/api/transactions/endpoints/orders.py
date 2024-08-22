from fastapi import APIRouter, Depends, HTTPException
from app.core import security
from app.core.jwt import JWTBearer
from app.api.deps import get_db
from sqlalchemy.orm import Session
from app.core.api_response import ApiResponse
from app.api.transactions.services.orders import OrdersService
from app.api.orders.services.customer import customer
from app.api.orders.schemas.order import OrderBase

router = APIRouter(prefix="/orders")


@router.get("/weekly", dependencies=[Depends(JWTBearer())])
def get_weekly_orders(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token
        order_service = OrdersService()
        weekly_orders = order_service.get_weekly_orders(db, token)

        orders_with_customer_info = []

        for weekly_order in weekly_orders:
            # Fetch the customer details using customer_id from the order
            customer_details = customer.get(db, weekly_order.customer_id)
            order_data = OrderBase.model_validate(weekly_order).model_dump()

            # Add customer_name to the order data if customer details are found
            order_data["customer_name"] = (
                customer_details.name if customer_details else None
            )

            orders_with_customer_info.append(order_data)

        return ApiResponse.response_ok(data=orders_with_customer_info)
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
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
