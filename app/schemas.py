from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class ProductSchema(BaseModel):
    id: Optional[int]=None
    name: Optional[str]=None
    buying_price: Optional[int]=None
    selling_price: Optional[int]=None
    description: Optional[str]=None
    image_url: Optional[str]=None

    class Config:
        orm_mode = True

class RequestProduct(BaseModel):
    parameter: ProductSchema = Field(...)


class Response (GenericModel, Generic[T]):
    code: str
    status: str 
    message: str
    result: Optional[T]           

