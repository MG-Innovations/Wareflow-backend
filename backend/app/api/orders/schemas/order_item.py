
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class OrderItemBase(BaseModel):
    id: UUID
    product_id: UUID
    order_id: UUID
    quantity: int
    price: float
    tenant_id: UUID

    class Config:
        from_attributes = True

class OrderItemCreateInDb(BaseModel):
    product_id: UUID
    order_id: UUID
    quantity: int
    price:float
    tenant_id: UUID