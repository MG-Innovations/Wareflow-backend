from fastapi import APIRouter
from .product import product_router

router = APIRouter()
router.include_router(product_router, prefix="/product" , tags=["Products"])

__all__ = ["router"]
