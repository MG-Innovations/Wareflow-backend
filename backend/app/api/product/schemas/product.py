from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True

class CompanyGet(BaseModel):
    id: UUID  #I want UUID 

class CompanyGetResponse(BaseModel):
    id: UUID 
    name: str
    email: str
    phone_number: str
    class Config:
        from_attributes = True

class CompanyDelete(BaseModel):
    id: UUID  #I want UUID here

class ProductType(BaseModel):
    name: str
    description: str
     
    class Config:
        from_attributes = True

class ProductTypeGet(BaseModel):
    id: UUID  #I want UUID here

class ProductTypeDelete(BaseModel):
    id: UUID  #I want UUID here

class Product(BaseModel):
    name: str
    description: str
    buying_price: float
    selling_price: float
    image: str
    stock: int
    company_id: UUID
    product_type_id: UUID

    class Config:
        from_attributes = True

class ProductGet(BaseModel):
    id: UUID  #I want UUID here

class ProductDelete(BaseModel):
    id: UUID  #I want UUID here