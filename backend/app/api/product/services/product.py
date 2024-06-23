from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.product.db_models.company import Company
from app.api.product.db_models.product_type import ProductType
from app.api.product.db_models.product import Product
from app.api.product.schemas.product import CompanyBase, ProductType as ProductTypeSchema, Product as ProductSchema

class ProductService:

    def create_company(self, db: Session, company: CompanyBase) -> Company:
        db_company = Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company

    # def get_companies(self, db: Session) -> List[Company]:
    #     return db.query(Company).all()

    # def get_company(self, db: Session, company_id: UUID) -> Optional[Company]:
    #     return db.query(Company).filter(Company.id == company_id).first()

    # def create_product_type(self, db: Session, product_type: ProductTypeSchema, user_id: UUID) -> ProductType:
    #     db_product_type = ProductType(**product_type.dict(), created_by=user_id, updated_by=user_id)
    #     db.add(db_product_type)
    #     db.commit()
    #     db.refresh(db_product_type)
    #     return db_product_type

    # def get_product_types(self, db: Session) -> List[ProductType]:
    #     return db.query(ProductType).all()

    # def get_product_type(self, db: Session, product_type_id: UUID) -> Optional[ProductType]:
    #     return db.query(ProductType).filter(ProductType.id == product_type_id).first()

    # def create_product(self, db: Session, product: ProductSchema, user_id: UUID) -> Product:
    #     db_product = Product(**product.dict(), created_by=user_id, updated_by=user_id)
    #     db.add(db_product)
    #     db.commit()
    #     db.refresh(db_product)
    #     return db_product

    # def get_products(self, db: Session) -> List[Product]:
    #     return db.query(Product).all()

    # def get_product(self, db: Session, product_id: UUID) -> Optional[Product]:
    #     return db.query(Product).filter(Product.id == product_id).first()

    # def delete_product(self, db: Session, product_id: UUID) -> Optional[UUID]:
    #     product = db.query(Product).filter(Product.id == product_id).first()
    #     if product:
    #         db.delete(product)
    #         db.commit()
    #         return product_id
    #     return None

product_service = ProductService()