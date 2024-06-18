from sqlalchemy.orm import Session
from ..models import Product
from ..v1.request.product import CreateProductSchema, UpdateProduct
from fastapi import HTTPException
import datetime
import uuid


class ProductService:
    def __init__(self): ...

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, product: CreateProductSchema):
        print("Here")
        _product = Product(
            id=uuid.uuid4(),
            name=product.name,
            buying_price=product.buying_price,
            selling_price=product.selling_price,
            description=product.description,
            image_url=product.image_url,
        )
        print(_product)
        db.add(_product)
        db.commit()
        db.refresh(_product)
        return _product

    def update_product(db: Session, product_id: str, product_request: UpdateProduct):
        product = db.query(Product).filter(Product.id == product_id).first()
        print(product)
        print(product_request)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product_request.name is not None:
            product.name = product_request.name
        if product_request.description is not None:
            product.description = product_request.description
        if product_request.image_url is not None:
            product.image_url = product_request.image_url
        if product_request.buying_price is not None:
            product.buying_price = product_request.buying_price
        if product_request.selling_price is not None:
            product.selling_price = product_request.selling_price

        db.commit()
        db.refresh(product)
        return product
