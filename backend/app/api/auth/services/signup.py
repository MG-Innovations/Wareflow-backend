from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from app.api.auth.schemas.token import Token
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.schemas.signup import UserSignupSchema, TenantSignupSchema
# from app.api.auth.crud.user import CRUDUser
from app.api.auth.crud.tenant import tenant
from app.api.auth.crud.user import user
from app.core.config import settings
router = APIRouter(prefix="/signup")


@router.post("/user",response_model=Token)
def signupUser(db:Session = Depends(deps.get_db),schema:UserSignupSchema = Depends()):
    base_user = user.create_user(db,tenant_schema=schema)

    if not base_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            base_user.id,expires_delta=access_token_expires
        ),
        "token_type":"Bearer"
    }


@router.post("/tenant",response_model=Token)
def signupTenant(db:Session = Depends(deps.get_db),schema:TenantSignupSchema = Depends()):
    base_tenant = tenant.create_tenant(db, schema=schema)

    if not base_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            base_tenant.id,expires_delta=access_token_expires
        ),
        "token_type":"Bearer"
    }
