from app.api.product.schemas.product import CompanyBase, CompanyGet, CompanyDelete, ProductType, ProductTypeGet, ProductTypeDelete, Product, ProductGet, ProductDelete , CompanyGetResponse
from app.core import security
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.core.jwt import JWTBearer
from app.core.api_response import ApiResponse
from app.core import security
from app.api.product.services.product import product_service

router = APIRouter(prefix="/product")
    
# Company Endpoints
@router.post("/company", dependencies=[Depends(JWTBearer())])
def create_company(company: CompanyBase, db: Session = Depends(get_db)):
    try:
        new_company = product_service.create_company(db, company)
        return ApiResponse.response_created(data=CompanyBase.model_validate(new_company).model_dump())
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/company/{company_id}", dependencies=[Depends(JWTBearer())])
def get_company(company_id: UUID , db: Session = Depends(get_db)):
    try:
        company = product_service.get_company_by_id(db, company_id)
        if company:
            return ApiResponse.response_ok(data=CompanyGetResponse.model_validate(company).model_dump())
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/company", dependencies=[Depends(JWTBearer())])
def get_all_companies(db: Session = Depends(get_db)):
    try:
        companies = product_service.get_companies(db)
        return ApiResponse.response_ok(data=[CompanyGetResponse.model_validate(company).model_dump() for company in companies])
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.delete("/company/{company_id}", dependencies=[Depends(JWTBearer())])
def delete_company(company_id: UUID, db: Session = Depends(get_db)):
    try:
        company = product_service.get_company_by_id(db, company_id)
        if company:
            result = product_service.delete_company(db, company_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

# Product Type Endpoints
@router.post("/product_type", dependencies=[Depends(JWTBearer())])
def create_product_type(product_type: ProductType, db: Session = Depends(get_db)):
    try:
        new_product_type = product_service.create_product_type(db, product_type)
        return ApiResponse.response_created(data=ProductType.model_validate(new_product_type).model_dump())
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

@router.get("/product_type/{product_type_id}", dependencies=[Depends(JWTBearer())])
def get_product_type(product_type_id: UUID , db: Session = Depends(get_db)):
    try:
        product_type = product_service.get_product_type_by_id(db, product_type_id)
        if product_type:
            return ApiResponse.response_ok(data=ProductType.model_validate(product_type).model_dump())
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/product_type", dependencies=[Depends(JWTBearer())])
def get_all_product_types(db: Session = Depends(get_db)):
    try:
        product_types = product_service.get_product_types(db)
        return ApiResponse.response_ok(data=[ProductType.model_validate(product_type).model_dump() for product_type in product_types])
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

@router.delete("/product_type/{product_type_id}", dependencies=[Depends(JWTBearer())])
def delete_product_type(product_type_id: UUID, db: Session = Depends(get_db)):
    try:
        product_type = product_service.get_product_type_by_id(db, product_type_id)
        if product_type:
            result = product_service.delete_product_type(db, product_type_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
# Product Endpoints

@router.post("/product", dependencies=[Depends(JWTBearer())])
def create_product(product: Product, db: Session = Depends(get_db) , auth_token: str = Depends(JWTBearer())):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get('user_id')

        tenant_id = payload.get('tenant_id')
        
        new_product = product_service.create_product(db, product , user_id,tenant_id)
        return ApiResponse.response_created(data=Product.model_validate(new_product).model_dump())
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/product/{product_id}", dependencies=[Depends(JWTBearer())])
def get_product(product_id: UUID , db: Session = Depends(get_db)):
    try:
        product = product_service.get_product_by_id(db, product_id)
        if product:
            return ApiResponse.response_ok(data=Product.model_validate(product).model_dump())
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
    
@router.get("/product", dependencies=[Depends(JWTBearer())])
def get_all_products(db: Session = Depends(get_db)):
    try:
        products = product_service.get_products(db)
        return ApiResponse.response_ok(data=[Product.model_validate(product).model_dump() for product in products])
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))

@router.delete("/product/{product_id}", dependencies=[Depends(JWTBearer())])
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