from fastapi import APIRouter
from .product import product_router

router = APIRouter()
router.include_router(product_router, prefix="/product")

__all__ = ["router"]
