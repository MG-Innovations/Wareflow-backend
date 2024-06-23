
from uuid import UUID
from pydantic import BaseModel
from app.api.orders.schemas.order_item import OrderItemBase 
from datetime import datetime


class OrderBase(BaseModel):
    id: UUID
    order_items: list[OrderItemBase]
    customer_id: UUID
    order_value: float
    tenant_id: UUID
    created_by: UUID
    updated_by: UUID

    class Config:
        from_attributes = True

        
class OrderItemCreateApi(BaseModel):
    product_id: UUID
    price: float
    quantity: float

class OrderItemCreate(BaseModel):
    product_id: UUID
    price: float
    quantity: float
    tenant_id: UUID

class OrderCreate(BaseModel):
    order_value: float
    customer_id: UUID
    tenant_id: UUID
    order_items: list[OrderItemCreateApi]    

class OrderCreateInDb(BaseModel):
    order_value: float
    customer_id: UUID
    created_by:UUID
    updated_by:UUID
    tenant_id:UUID

