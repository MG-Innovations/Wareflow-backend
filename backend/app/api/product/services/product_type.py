from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.product.db_models.product_type import ProductType
from app.api.product.schemas.product_type import (
    ProductType as ProductTypeSchema,
)


class ProductTypeService:
    def create_product_type(
        self, db: Session, product_type: ProductTypeSchema
    ) -> ProductType:
        db_product_type = ProductType(**product_type.dict())
        db.add(db_product_type)
        db.commit()
        db.refresh(db_product_type)
        return db_product_type

    def get_product_types(self, db: Session,query:str) -> List[ProductType]:
        return db.query(ProductType).where(ProductType.name.like(f"%{query}%")).all()

    def get_product_type_by_id(
        self, db: Session, product_type_id: UUID
    ) -> Optional[ProductType]:
        return db.query(ProductType).filter(ProductType.id == product_type_id).first()

    def delete_product_type(self, db: Session, product_type_id: UUID) -> Optional[UUID]:
        product_type = (
            db.query(ProductType).filter(ProductType.id == product_type_id).first()
        )
        if product_type:
            db.delete(product_type)
            db.commit()
            return product_type_id
        return None


product_type_service = ProductTypeService()
