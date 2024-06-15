from sqlalchemy.orm import Session
from ..models import Product
from ..v1.request.product import ProductSchema

class ProductService:
    def __init__(self):
        ...

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, product: ProductSchema):
        _product = Product(
            name=product.name,
            buying_price=product.buying_price,
            selling_price=product.selling_price,
            description=product.description,
            image_url=product.image_url
        )
        print(_product)
        db.add(_product)
        db.commit()
        db.refresh(_product)
        return _product
