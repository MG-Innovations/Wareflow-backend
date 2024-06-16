from fastapi import APIRouter

from api.tenant.v1.router import router as tenant_v1_router
from api.products.v1.router import router as product_v1_router

router = APIRouter()

router.include_router(product_v1_router, prefix="/v1", tags=["Products"])
router.include_router(tenant_v1_router, prefix="/v1", tags=["Tenants"])

__all__ = ["router"]
