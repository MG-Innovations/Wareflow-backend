from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.product.db_models.company import Company
from app.api.product.db_models.product_type import ProductType
from app.api.product.db_models.product import Product
from app.api.product.schemas.product import (
    Product as ProductSchema,
)


class ProductService:

    def create_product(
        self, db: Session, product: ProductSchema, user_id, tenant_id
    ) -> Product:
        db_product = Product(
            **product.model_dump(),
            tenant_id=tenant_id,
            created_by=user_id,
            updated_by=user_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    def get_products(self, db: Session,tenant_id:UUID,skip:int=0,limit:int=10) -> List[Product]:
        return db.query(Product).filter_by(tenant_id=tenant_id).offset(skip).limit(limit).all()
    
    def get_product_by_id(self, db: Session, product_id: UUID) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    def delete_product(self, db: Session, product_id: UUID) -> Optional[UUID]:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return product_id
        return None

product_service = ProductService()
