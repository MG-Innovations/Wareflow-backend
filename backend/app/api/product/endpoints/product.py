from app.api.product.schemas.product import CompanyBase, CompanyGet, CompanyDelete, ProductType, ProductTypeGet, ProductTypeDelete, Product, ProductGet, ProductDelete
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
        return ApiResponse.response_ok(data=CompanyBase.model_validate(new_company).model_dump())
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))