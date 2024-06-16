from fastapi import APIRouter
from .tenant import tenant_router

router = APIRouter()
router.include_router(tenant_router, prefix="/tenant" , tags=["Tenants"])

__all__ = ["router"]
