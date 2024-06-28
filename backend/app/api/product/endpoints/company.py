from app.api.product.schemas.company import (
    CompanyBase,
    CompanyGet,
    CompanyDelete,
    CompanyGetResponse,
)
from app.core import security
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.core.jwt import JWTBearer
from app.core.api_response import ApiResponse
from app.core import security
from app.api.product.services.company import company_service


router = APIRouter(prefix="/company")


@router.post("/", dependencies=[Depends(JWTBearer())])
def create_company(company: CompanyBase, db: Session = Depends(get_db)):
    try:
        new_company = company_service.create_company(db, company)
        return ApiResponse.response_created(
            data=CompanyBase.model_validate(new_company).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/{company_id}", dependencies=[Depends(JWTBearer())])
def get_company(company_id: UUID, db: Session = Depends(get_db)):
    try:
        company = company_service.get_company_by_id(db, company_id)
        if company:
            return ApiResponse.response_ok(
                data=CompanyGetResponse.model_validate(company).model_dump()
            )
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_companies(db: Session = Depends(get_db)):
    try:
        companies = company_service.get_companies(db)
        return ApiResponse.response_ok(
            data=[
                CompanyGetResponse.model_validate(company).model_dump()
                for company in companies
            ]
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.delete("/{company_id}", dependencies=[Depends(JWTBearer())])
def delete_company(company_id: UUID, db: Session = Depends(get_db)):
    try:
        company = company_service.get_company_by_id(db, company_id)
        if company:
            result = company_service.delete_company(db, company_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
