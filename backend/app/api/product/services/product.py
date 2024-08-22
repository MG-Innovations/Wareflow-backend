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
        search: str = "",
        filter1: str = "",
        filter2: str = "",
    ) -> List[Product]:
        filters = [Product.tenant_id == tenant_id]

        if search:
            filters.append(Product.name.like(f"%{search}%"))
        if filter1:
            filters.append(Company.name.like(f"%{filter1}%"))
        if filter2:
            filters.append(ProductType.name.like(f"%{filter2}%"))
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
