from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class Product(BaseModel):
    name: str
    description: str
    buying_price: float
    selling_price: float
    image: Optional[str]
    stock: int
    company_id: UUID
    product_type_id: UUID

    class Config:
        from_attributes = True


class ProductGet(BaseModel):
    id: UUID  # I want UUID here


class ProductDelete(BaseModel):
    id: UUID  # I want UUID here


class ProductGetDetailResponse(BaseModel):
    id: UUID
    name: str
    description: str
    buying_price: float
    selling_price: float
    image: str
    stock: int
    company_id: UUID
    company: str
    product_type_id: UUID
    product_type: str

    class Config:
        from_attributes = True
