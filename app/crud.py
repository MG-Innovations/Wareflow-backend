from sqlalchemy.orm import Session
from model import Product
from schemas import ProductSchema

def get_all_products(db:Session,skip:int=0, limit:int=10):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db:Session, product: ProductSchema):
    _product = Product(
        name=product.name,
        buying_price=product.buying_price,
        selling_price=product.selling_price,
        description=product.description,
        image_url=product.image_url)
    db.add(_product)
    db.commit()
    db.refresh(_product)
    return _product


