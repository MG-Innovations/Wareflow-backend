from datetime import timedelta
from typing import Annotated
from uuid import UUID
from app.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.orders.services.customer import customer 
from app.api.orders.schemas.customer import CustomerCreate,CustomerCreateInDb, CustomerBase
from app.core.api_response import ApiResponse
from app.core.config import settings
from app.core.jwt import JWTBearer


router = APIRouter(prefix="/customer")



@router.post("/",dependencies=[Depends(JWTBearer())])
async def create(db:Session = Depends(deps.get_db),data:CustomerCreate = Body(...),auth_token: str = Depends(JWTBearer())):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get('sub')
        
        customer_db_base = CustomerCreateInDb(
            name = data.name,
            phone_number = data.phone_number,
            tenant_id = data.tenant_id,
            created_by = user_id,
            updated_by = user_id
        )
    
        base_customer = customer.create(db,customer_db_base)

        if not base_customer:
            return ApiResponse.response_bad_request()
        
        return ApiResponse.response_ok(
                data=CustomerBase.model_validate(base_customer).model_dump(),
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

    
@router.get("/{customer_id}",dependencies=[Depends(JWTBearer())])
def get_user(customer_id:UUID,db: Session = Depends(deps.get_db),auth_token: str = Depends(JWTBearer())):
    try:
        base_customer = customer.get(db,customer_id)
        if not base_customer:
            return ApiResponse.response_bad_request()
        
        return ApiResponse.response_ok(
            data=CustomerBase.model_validate(base_customer).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))    