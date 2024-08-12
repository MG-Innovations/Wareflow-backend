from datetime import timedelta
from typing import Annotated
from uuid import UUID
from app.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.orders.services.order import order
from app.api.orders.schemas.order import (
    OrderCreate,
    OrderCreateInDb,
    OrderItemCreate,
    OrderBase,
)
from app.core.api_response import ApiResponse
from app.core.config import settings
from app.core.jwt import JWTBearer
from app.api.orders.services.customer import customer
from app.api.orders.schemas.customer import CustomerBase
from app.api.orders.db_models.order import Order


router = APIRouter(prefix="/order")


@router.post("/", dependencies=[Depends(JWTBearer())])
async def create(
    db: Session = Depends(deps.get_db),
    data: OrderCreate = Body(...),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get("user_id")

        tenant_id = payload.get("tenant_id")

        order_db_base = OrderCreateInDb(
            customer_id=data.customer_id,
            order_value=data.order_value,
            tenant_id=tenant_id,
            created_by=user_id,
            updated_by=user_id,
        )

        order_items = [
            OrderItemCreate(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                tenant_id=tenant_id,
            )
            for item in data.order_items
        ]

        base_order = order.create_order_with_items(db, order_db_base, order_items)

        if not base_order:
            return ApiResponse.response_bad_request()

        return ApiResponse.response_created(
            data=OrderBase.model_validate(base_order).model_dump(),
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all(
    limit: int,
    offset: int,
    db: Session = Depends(deps.get_db),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        tenant_id = security.decode_access_token(auth_token).get("tenant_id")
        offset = offset * limit
        base_orders = order.get_all(db, tenant_id=tenant_id, limit=limit, skip=offset)
        if not base_orders:
            return ApiResponse.response_bad_request()

        orders_with_customer_info = []
        completed_orders = 0
        incomplete_orders = 0
        total_revenue = 0

        all_orders_len = db.query(Order).all()

        for base_order in base_orders:
            customer_details = customer.get(db, base_order.customer_id)
            order_data = OrderBase.model_validate(base_order).model_dump()
            order_data["customer_details"] = (
                CustomerBase.model_validate(customer_details).model_dump()
                if customer_details
                else None
            )
            order_data["order_items_count"] = len(base_order.order_items)

            # Calculate completed and incomplete orders
            if base_order.status.lower() == "paid":
                completed_orders += 1
            elif base_order.status.lower() in ["unpaid", "partially paid"]:
                incomplete_orders += 1

            # Add to total revenue
            total_revenue += base_order.order_value

            orders_with_customer_info.append(order_data)

        total_orders = len(all_orders_len)

        response_data = {
            "orders": orders_with_customer_info,
            "completed_orders": completed_orders,
            "incomplete_orders": incomplete_orders,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
        }

        return ApiResponse.response_ok(data=response_data)
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/unpaid_orders", dependencies=[Depends(JWTBearer())])
def get_unpaid_orders(
    db: Session = Depends(deps.get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        tenant_id = security.decode_access_token(auth_token).get("tenant_id")
        unpaid_orders = order.get_unpaid_orders(db, tenant_id=tenant_id)
        if not unpaid_orders:
            return ApiResponse.response_bad_request()

        orders_with_customer_info = []

        for unpaid_order in unpaid_orders:
            # Fetch the customer details using customer_id from the order
            customer_details = customer.get(db, unpaid_order.customer_id)
            order_data = OrderBase.model_validate(unpaid_order).model_dump()

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


@router.get("/{order_id}", dependencies=[Depends(JWTBearer())])
def get_user(
    order_id: UUID,
    db: Session = Depends(deps.get_db),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        base_order = order.get(db, order_id)
        if not base_order:
            return ApiResponse.response_bad_request()

        return ApiResponse.response_ok(
            data=OrderBase.model_validate(base_order).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
