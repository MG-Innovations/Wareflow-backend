from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class UserBase(BaseModel):
    name: str
    email: str
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

class UserDelete(UserBase):
    id: UUID  




