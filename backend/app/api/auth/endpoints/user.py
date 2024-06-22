from datetime import timedelta
from typing import Annotated
from app.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlalchemy.orm import Session  # type: ignore
from app.core import security
from app.api import deps
from app.api.auth.services.user import user
from app.api.auth.schemas.user import UserGet, UserLogin, UserCreate, UserLoginResponse
from app.core.api_response import ApiResponse
from app.core.config import settings
from app.core.jwt import JWTBearer


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
        
        schema = UserLoginResponse()

        schema.access_token = access_token
        schema.token_type = "bearer"
        schema.user = UserGet.from_orm(base_user)

        return ApiResponse.response_ok(
                data={
                    "access_token": schema.access_token,
                    "token_type": schema.token_type,
                    "user": schema.user.name
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
            data=UserCreate.from_orm(base_user)
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

    
@router.get("/",dependencies=[Depends(JWTBearer())])
def get_tenant(db: Session = Depends(deps.get_db),auth_token: str = Depends(JWTBearer())):
    try:
        # Decode the JWT token from Header\
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get('sub')
        
        base_user = user.get_user(db, user_id)
        if not base_user:
            return ApiResponse.response_bad_request()
        
        return ApiResponse.response_ok(
            data=UserGet.from_orm(base_user)
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(
            status=e.status_code,
            message=e.detail,
        )
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))    