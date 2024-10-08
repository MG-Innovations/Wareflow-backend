from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from app.core.enums import PaymentType
class Payment(BaseModel):
    amount_paid: float
    payment_type: PaymentType 
    order_id: UUID
    description : str

    class Config:
        from_attributes = True

class PaymentGet(BaseModel):
    id: UUID  #I want UUID here

class PaymentGetResponse(BaseModel):
    id: UUID 
    amount_paid: float
    payment_type: str
    tenant_id: UUID
    order_id: UUID
    user_id: UUID
    customer_name: Optional[str] = None
    description : str
    
    class Config:
        from_attributes = True

class PaymentUpdate(BaseModel):
    id: UUID  
    amount_paid: float
    tenant_id: UUID
    order_id: UUID
    description : str

    class Config:
        from_attributes = True

class PaymentDelete(BaseModel):
    id: UUID  #I want UUID here