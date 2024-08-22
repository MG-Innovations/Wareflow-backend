from app.api.product.schemas.product import (
    Product,
    ProductGetDetailResponse,
    ProductUpdateRequest
)
from app.core import security
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.core.jwt import JWTBearer
from app.core.api_response import ApiResponse
from app.core import security
from app.api.product.services.product import product_service
from typing import Optional

router = APIRouter(prefix="/product")


@router.post("/", dependencies=[Depends(JWTBearer())])
def create_product(
    product: Product,
    db: Session = Depends(get_db),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get("user_id")

        tenant_id = payload.get("tenant_id")

        new_product = product_service.create_product(db, product, user_id, tenant_id)
        return ApiResponse.response_created(
            data=Product.model_validate(new_product).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/{product_id}", dependencies=[Depends(JWTBearer())])
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    try:
        product = product_service.get_product_by_id(db, product_id)
        if product:
            return ApiResponse.response_ok(
                data=ProductGetDetailResponse.model_validate(product).model_dump()
            )
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_products(
    search: Optional[str] = Query(None),
    filter1: Optional[str] = Query(None),
    filter2: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        tenant_id = security.decode_access_token(auth_token).get("tenant_id")
        products = product_service.get_products(
            db, tenant_id=tenant_id, search=search, filter1=filter1, filter2=filter2
        )
        return ApiResponse.response_ok(
            data=[ProductGetDetailResponse.model_validate(product).model_dump() for product in products]
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.delete("/{product_id}", dependencies=[Depends(JWTBearer())])
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    try:
        product = product_service.get_product_by_id(db, product_id)
        if product:
            result = product_service.delete_product(db, product_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.put('/{product_id}',dependencies=[Depends(JWTBearer())])    
def update_product(
    product_id:UUID,
    product_context:ProductUpdateRequest,
    db: Session = Depends(get_db),
    auth_token = Depends(JWTBearer()),
):
    try:
        decoded_token = security.decode_access_token(auth_token)
        user_id = decoded_token.get("user_id")
        product_service.updateProduct(
            db=db,
            user_id=user_id, 
            name=product_context.name,
            description=product_context.description,
            buying_price=product_context.buying_price,
            selling_price=product_context.selling_price,
            image=product_context.image,
            stock=product_context.stock,
            product_id=product_id
        )
        return ApiResponse.response_ok()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
