from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class ProductType(BaseModel):
    id: Optional[UUID]
    name: str
    description: str

    class Config:
        from_attributes = True


class ProductTypeGet(BaseModel):
    id: UUID


class ProductTypeDelete(BaseModel):
    id: UUID
