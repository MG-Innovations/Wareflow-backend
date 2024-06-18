from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.services.user import user
from app.api.auth.schemas.user import UserLogin, UserCreate
from app.core.api_response import ApiResponse
from app.core.config import settings
router = APIRouter(prefix="/user")



@router.post("/login")
async def loginUser(db:Session = Depends(deps.get_db),login:UserLogin = Body(...)):
    try:
        base_user = user.authenticate(db, email=login.email, password=login.password)

        if not base_user:
            return ApiResponse.response_bad_request()
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        access_token = security.create_access_token(
                base_user.id, expires_delta=access_token_expires
            )
        return ApiResponse.response_ok(
                data={
                    "access_token": access_token,
                    "token_type": "Bearer",
                    "tenant": base_user.dict()
                }
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.post("/signup")
async def signupUser(db:Session = Depends(deps.get_db),schema:UserCreate = Body(...)):
    try:
        base_user = user.create_user(db, schema=schema)
        if not base_user:
            return ApiResponse.response_bad_request()
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            base_user.id, expires_delta=access_token_expires
        )

        return ApiResponse.response_created(
            data={
                "access_token": access_token,
                "token_type": "Bearer",
                "tenant": base_user.dict()
            }
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
