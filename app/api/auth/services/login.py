from datetime import timedelta
from fastapi import APIRouter, Depends, Any, status, HTTPException
from app.api.auth.schemas.token import Token
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.schemas.login import Login
from auth.crud.user import CRUDUser 
from app.core.config import settings
router = APIRouter()



@router.post("/login/user/",response_model=Token)
def loginUser(db:Session = Depends(deps.get_db),login:Login = Depends())->Any:
    user = CRUDUser.authenticate(db, email=login.email, password=login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id,expires_delta=access_token_expires
        ),
        "token_type":"Bearer"
    }


@router.post("/login/tenant/",response_model=Token)
def loginTenant(db:Session = Depends(deps.get_db),login:Login = Depends())->Any:
    user = CRUDUser.authenticate(db, email=login.email, password=login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id,expires_delta=access_token_expires
        ),
        "token_type":"Bearer"
    }
