from datetime import timedelta
from fastapi import APIRouter, Depends, Header, status, HTTPException, Body
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.schemas.tenant import TenantLogin, TenantCreate
from app.api.auth.services.tenant import tenant
from app.core.config import settings
from app.core.api_response import ApiResponse

router = APIRouter(prefix="/tenant")

@router.post("/signup")
def signup_tenant(db: Session = Depends(deps.get_db), schema: TenantCreate = Body(...)):
    try:
        base_tenant = tenant.create_tenant(db, schema=schema)
        if not base_tenant:
            return ApiResponse.response_bad_request()

        return ApiResponse.response_created(
            data={
                "id": base_tenant.id.toString(),
            }
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/")
def get_tenant(db: Session = Depends(deps.get_db)):
    try:
        # Decode the JWT token from Header\
        token = authorization.split(" ")[1]

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        tenant_id = payload.get('sub')
        base_tenant = tenant.get_tenant(db, tenant_id)
        if not base_tenant:
            return ApiResponse.response_bad_request()
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            base_tenant.id, expires_delta=access_token_expires
        )

        return ApiResponse.response_created(
            data={
                "access_token": access_token,
                "token_type": "Bearer",
            }
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))    
