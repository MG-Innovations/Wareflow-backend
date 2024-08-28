from typing import Optional
from app.api.product.schemas.product_type import (
    ProductType,
    ProductTypeGet,
    ProductTypeDelete,
)
from app.core import security
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.core.jwt import JWTBearer
from app.core.api_response import ApiResponse
from app.core import security
from app.api.product.services.product_type import product_type_service

router = APIRouter(prefix="/product_type")


@router.post("/", dependencies=[Depends(JWTBearer())])
def create_product_type(product_type: ProductType, db: Session = Depends(get_db)):
    try:
        new_product_type = product_type_service.create_product_type(db, product_type)
        return ApiResponse.response_created(
            data=ProductType.model_validate(new_product_type).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/{product_type_id}", dependencies=[Depends(JWTBearer())])
def get_product_type(product_type_id: UUID, db: Session = Depends(get_db)):
    try:
        product_type = product_type_service.get_product_type_by_id(db, product_type_id)
        if product_type:
            return ApiResponse.response_ok(
                data=ProductType.model_validate(product_type).model_dump()
            )
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_product_types(
    query:Optional[str] = Query(""),
    db: Session = Depends(get_db)):
    try:
        product_types = product_type_service.get_product_types(db,query=query)
        return ApiResponse.response_ok(
            data=[
                ProductTypeGet.model_validate(product_type).model_dump()
                for product_type in product_types
            ]
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.delete("/{product_type_id}", dependencies=[Depends(JWTBearer())])
def delete_product_type(product_type_id: UUID, db: Session = Depends(get_db)):
    try:
        product_type = product_type_service.get_product_type_by_id(db, product_type_id)
        if product_type:
            result = product_type_service.delete_product_type(db, product_type_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
