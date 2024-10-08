from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.product.db_models.company import Company
from app.api.product.db_models.product_type import ProductType
from app.api.product.db_models.product import Product
from app.api.product.schemas.product import (
    Product as ProductSchema,
)
from sqlalchemy import select, and_, or_,update


class ProductService:

    def create_product(
        self, db: Session, product: ProductSchema, user_id, tenant_id
    ) -> Product:
        db_product = Product(
            **product.model_dump(),
            tenant_id=tenant_id,
            created_by=user_id,
            updated_by=user_id,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_products(
        self,
        db: Session,
        tenant_id: UUID,
        product_type_id: UUID = None,
        company_id: UUID = None,
        search: str = None,

    ) -> List[Product]:
        filters = [Product.tenant_id == tenant_id]
        if search:
            filters.append(Product.name.like(f"%{search}%"))
        
        if product_type_id:
            filters.append(Product.product_type_id == product_type_id)
        
        if company_id:
            filters.append(Product.company_id == company_id)        
        stmt = (
            select(
                Product.id,
                Product.name,
                Product.description,
                Product.buying_price,
                Product.selling_price,
                Product.image,
                Product.stock,
                Product.company_id,
                Company.name.label("company_name"),
                Product.product_type_id,
                ProductType.name.label("product_type_name"),
            )
            .select_from(Product)
            .join(Company, Product.company_id == Company.id)
            .join(ProductType, Product.product_type_id == ProductType.id)
            .limit(40)
        ).filter(and_(*filters))
        results = db.execute(stmt)
        products = []
        for row in results:
            data = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "buying_price": row.buying_price,
                "selling_price": row.selling_price,
                "image": row.image,
                "stock": row.stock,
                "company_id": row.company_id,
                "company": row.company_name,
                "product_type_id": row.product_type_id,
                "product_type": row.product_type_name,
            }
            products.append(data)
        return products

    def get_product_by_id(self, db: Session, product_id: UUID) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    def delete_product(self, db: Session, product_id: UUID) -> Optional[UUID]:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return product_id
        return None
    
    def updateProduct(
        self,
        db:Session,
        user_id:UUID,
        product_id:UUID,
        name:str,
        description: str,
        buying_price: float,
        product_type_id:UUID,
        company_id:UUID,
        selling_price: float,
        image: str,
        stock: int,
    ):
     
        update_values = {key: value for key, value in locals().items() 
                        if key not in ['self', 'user_id','db','product_id'] and value is not None}
                
        update_values['updated_by'] = user_id 
        
        update_product_query = (
            update(Product)
            .where(Product.id == product_id)
            .values(**update_values)
        )
        
        db.execute(update_product_query)
        db.commit()
        return
        
        


product_service = ProductService()
