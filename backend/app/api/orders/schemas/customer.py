
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class CustomerBase(BaseModel):
    id: UUID
    name: str
    phone_number: str
    tenant_id: UUID
    created_by: UUID
    updated_by: UUID

    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    tenant_id: UUID        

class CustomerCreateInDb(BaseModel):
    name:str
    phone_number: str
    created_by:UUID
    updated_by:UUID
    tenant_id:UUID