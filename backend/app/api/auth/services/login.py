from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from app.api.auth.schemas.token import Token
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.schemas.login import Login
from app.api.auth.crud.user import user
from app.api.auth.crud.tenant import tenant
from app.core.config import settings
router = APIRouter(prefix="/login")


@router.post("/user",response_model=Token)
def loginUser(db:Session = Depends(deps.get_db),login:Login = Depends()):
    base_user = user.authenticate(db, email=login.email, password=login.password)

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
def loginTenant(db:Session = Depends(deps.get_db),login:Login = Depends()):
    base_tenant = tenant.authenticate(db, email=login.email, password=login.password)

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
        "token_type":"Bearer",
        "details": base_tenant
    }
