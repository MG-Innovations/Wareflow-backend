from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import ProductSchema, RequestProduct, Response
import crud


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post('/')
async def create(request: RequestProduct,db: Session=Depends(get_db)):
    crud.create_product(db, request.parameter)
    return Response(code="200", status="OK", message="Product created", result=request.parameter).dict(exclude_none=True)

@router.get('/')
async def get_all(db: Session=Depends(get_db)):
    products = crud.get_all_products(db,0,10)
    return Response(code="200", status="OK", message="Product Fetched", result=products).dict(exclude_none=True)