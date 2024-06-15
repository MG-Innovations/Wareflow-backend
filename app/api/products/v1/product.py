from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..services.product import ProductService
from ..v1.request.product import ProductSchema, RequestProduct, Response
from config import get_db

product_router = APIRouter()

@product_router.post('/')
async def create(request: RequestProduct, db: Session = Depends(get_db)):
    ProductService.create_product(db, request.parameter)
    return Response(code="200", status="OK", message="Product created", result=request.parameter).dict(exclude_none=True)

@product_router.get('/')
async def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = ProductService.get_all_products(db, skip, limit)
    return Response(code="200", status="OK", message="Products retrieved", result=products).dict(exclude_none=True)