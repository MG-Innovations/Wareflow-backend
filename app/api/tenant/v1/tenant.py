from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..services.tenant import TenantService
from ..v1.request.tenant import CreateTenantRequest, UpdateTenantRequest
from ..v1.response.tenant import Response
from config import get_db

tenant_router = APIRouter()


@tenant_router.post("/")
async def create_tenant(request: CreateTenantRequest, db: Session = Depends(get_db)):
    tenant = TenantService.create_tenant(db, request)
    return Response(
        code="200", status="OK", message="Tenant created", result=tenant
    ).dict(exclude_none=True)


@tenant_router.get("/{tenant_id}")
async def get_tenant_by_id(tenant_id: str, db: Session = Depends(get_db)):
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    return Response(
        code="200", status="OK", message="Tenant retrieved", result=tenant
    ).dict(exclude_none=True)


@tenant_router.get("/")
async def get_all_tenants(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    tenants = TenantService.get_all_tenants(db, skip, limit)
    return Response(
        code="200", status="OK", message="Tenants retrieved", result=tenants
    ).dict(exclude_none=True)


@tenant_router.put("/{tenant_id}")
async def update_tenant(
    tenant_id: str, request: UpdateTenantRequest, db: Session = Depends(get_db)
):
    tenant = TenantService.update_tenant(db, tenant_id, request)
    return Response(code="200", status="OK", message="Tenant updated").dict(
        exclude_none=True
    )


@tenant_router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: str, db: Session = Depends(get_db)):
    TenantService.delete_tenant(db, tenant_id)
    return Response(code="200", status="OK", message="Tenant deleted").dict(
        exclude_none=True
    )
