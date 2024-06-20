from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..services.product import ProductService
from ..v1.request.product import CreateProductSchema, UpdateProduct
from ..v1.response.product import Response
from config import get_db

product_router = APIRouter()


@product_router.post("/")
async def create_product(request: CreateProductSchema, db: Session = Depends(get_db)):
    product = ProductService.create_product(db, request)
    return Response(
        code="200", status="OK", message="Product created", result=product
    ).dict(exclude_none=True)


@product_router.put("/{product_id}")
async def update_product(
    product_id: str, request: UpdateProduct, db: Session = Depends(get_db)
):
    product = ProductService.update_product(db, product_id, request)
    return Response(
        code="200", status="OK", message="Product updated", result=product
    ).dict(exclude_none=True)


@product_router.get("/")
async def get_products(db: Session = Depends(get_db)):
    product = ProductService.getall_product(db)
    return Response(
        code="200", status="OK", message="All products fetched", result=product
    ).dict(exclude_none=True)


@product_router.get("/{product_id}")
async def get_product(product_id: str, db: Session = Depends(get_db)):
    product = ProductService.get_product(db, product_id)
    return Response(
        code="200", status="OK", message="All products fetched", result=product
    ).dict(exclude_none=True)


@product_router.delete("/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    ProductService.delete_product(db, product_id)
    return Response(
        code="200", status="OK", message="Product Deleted!!"
    ).dict(exclude_none=True)