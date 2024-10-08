from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class ProductType(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True



class ProductTypeGet(BaseModel):
    id: UUID
    name: str
    description: str
    
    class Config:
        from_attributes = True


class ProductTypeDelete(BaseModel):
    id: UUID
