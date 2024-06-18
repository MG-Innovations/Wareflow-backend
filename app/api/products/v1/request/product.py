from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class CreateProductSchema(BaseModel):
    name: str
    description: Optional[str]
    buying_price: int
    selling_price: Optional[int]
    image_url: Optional[str]


class UpdateProduct(BaseModel):
    name: Optional[str]
    description: Optional[str]
    company: Optional[str]
    image_url: Optional[str]
    buying_price: Optional[int]
    selling_price: Optional[int]
