from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class UserBase(BaseModel):
    id:  UUID
    name: str
    email: str
    tenant_id: UUID
    phone_number: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    name: str
    email: str
    tenant_id:UUID
    phone_number: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserGet(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str | None
    tenant_id:UUID

    class Config:
        from_attributes = True

class UserDelete(UserBase):
    id: UUID  




