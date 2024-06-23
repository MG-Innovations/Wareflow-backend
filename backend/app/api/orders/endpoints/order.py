from datetime import timedelta
from typing import Annotated
from uuid import UUID
from app.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.orders.services.order import order 
from app.api.orders.schemas.order import OrderCreate,OrderCreateInDb, OrderItemCreate, OrderBase
from app.core.api_response import ApiResponse
from app.core.config import settings
from app.core.jwt import JWTBearer


router = APIRouter(prefix="/order")



@router.post("/",dependencies=[Depends(JWTBearer())])
async def create(db:Session = Depends(deps.get_db),data:OrderCreate = Body(...),auth_token: str = Depends(JWTBearer())):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get('sub')
        
        order_db_base = OrderCreateInDb(
            customer_id = data.customer_id,
            order_value = data.order_value,
            tenant_id = data.tenant_id,
            created_by = user_id,
            updated_by = user_id
        )

        order_items = [
            OrderItemCreate(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                tenant_id=data.tenant_id
            ) for item in data.order_items
        ]
    
    
        base_order = order.create(db,order_db_base,order_items)

        if not base_order:
            return ApiResponse.response_bad_request()
        
        return ApiResponse.response_ok(
                data=OrderBase.model_validate(base_order).model_dump(),
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

    
# @router.get("/{customer_id}",dependencies=[Depends(JWTBearer())])
# def get_user(customer_id:UUID,db: Session = Depends(deps.get_db),auth_token: str = Depends(JWTBearer())):
#     try:
#         base_customer = customer.get(db,customer_id)
#         if not base_customer:
#             return ApiResponse.response_bad_request()
        
#         return ApiResponse.response_ok(
#             data=CustomerBase.model_validate(base_customer).model_dump()
#         )
#     except HTTPException as e:
#         return ApiResponse.response_bad_request(
#             status=e.status_code,
#             message=e.detail,
#         )
#     except Exception as e:
#         return ApiResponse.response_internal_server_error(message=str(e))    