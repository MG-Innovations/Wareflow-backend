from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..services.tenant import TenantService
from ..v1.request.tenant import CreateTenantRequest
from ..v1.response.tenant import Response
from config import get_db

tenant_router = APIRouter()

@tenant_router.post('/')
async def create(request: CreateTenantRequest, db: Session = Depends(get_db)):
    TenantService.create_tenant(db, request)
    return Response(code="200", status="OK", message="Product created", result=request).dict(exclude_none=True)

# @tenant_router.get('/')
# async def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     products = TenantService.get_all_products(db, skip, limit)
#     return Response(code="200", status="OK", message="Products retrieved", result=products).dict(exclude_none=True)