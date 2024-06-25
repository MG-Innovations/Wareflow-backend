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
    
    def get_company_by_id(self, db: Session, company_id: UUID) -> Optional[Company]:
        return db.query(Company).filter(Company.id == company_id).first()

    def get_companies(self, db: Session) -> List[Company]:
        return db.query(Company).all()
    
    def delete_company(self, db: Session, company_id: UUID) -> Optional[UUID]:
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            db.delete(company)
            db.commit()
            return company_id
        return None
    
    def create_product_type(self, db: Session, product_type: ProductTypeSchema) -> ProductType:
        db_product_type = ProductType(**product_type.dict())
        db.add(db_product_type)
        db.commit()
        db.refresh(db_product_type)
        return db_product_type
    
    def get_product_types(self, db: Session) -> List[ProductType]:
        return db.query(ProductType).all()
    
    def get_product_type_by_id(self, db: Session, product_type_id: UUID) -> Optional[ProductType]:
        return db.query(ProductType).filter(ProductType.id == product_type_id).first()
    
    def delete_product_type(self, db: Session, product_type_id: UUID) -> Optional[UUID]:
        product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
        if product_type:
            db.delete(product_type)
            db.commit()
            return product_type_id
        return None
    
    def create_product(self, db: Session, product: ProductSchema , user_id,tenant_id) -> Product:
        db_product = Product(**product.model_dump(),tenant_id=tenant_id,created_by=user_id, updated_by=user_id)
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