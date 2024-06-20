from fastapi import APIRouter
from .v1.router import router as v1_router

router = APIRouter()
router.include_router(v1_router, prefix="/v1" , tags=["Products"])

__all__ = ["router"]