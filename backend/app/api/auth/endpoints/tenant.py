from datetime import timedelta
from fastapi import APIRouter, Depends, Header, status, HTTPException, Body
from uuid import UUID
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.schemas.tenant import  TenantCreate, TenantGetResponse
from app.api.auth.services.tenant import tenant
from app.core.config import settings
from app.core.api_response import ApiResponse

router = APIRouter(prefix="/tenant")

@router.post("/create")
def signup_tenant(db: Session = Depends(deps.get_db), schema: TenantCreate = Body(...)):
    try:
        base_tenant = tenant.create_tenant(db, schema=schema)
        if not base_tenant:
            return ApiResponse.response_bad_request()

        return ApiResponse.response_created(
            data= TenantGetResponse.model_validate(base_tenant).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/{tenant_id}")
def get_tenant(tenant_id: UUID,db: Session = Depends(deps.get_db),):
    try:
        base_tenant = tenant.get_tenant(db, tenant_id)
        if not base_tenant:
            return ApiResponse.response_bad_request()
        
        return ApiResponse.response_ok(
            data=TenantGetResponse.model_validate(base_tenant).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))    
