from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: str

    class Config:
        orm_mode = True
        from_attributes = True

class CompanyGet(CompanyBase):
    id: UUID  #I want UUID here

class CompanyDelete(CompanyBase):
    id: UUID  #I want UUID here

class ProductType(BaseModel):
    name: str
    discrption: str

class ProductTypeGet(ProductType):
    id: UUID  #I want UUID here

class ProductTypeDelete(ProductType):
    id: UUID  #I want UUID here

class Product(BaseModel):
    name: str
    description: str
    buying_price: float
    selling_price: float
    image: str
    stock: str
    tenant_id: UUID
    company_id: UUID
    product_type_id: UUID

class ProductGet(Product):
    id: UUID  #I want UUID here

class ProductDelete(Product):
    id: UUID  #I want UUID here