from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class UserBase(BaseModel):
    id:  str
    name: str
    email: str
    tenant_id: str
    phone_number: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    name: str
    email: str
    tenant_id:str
    phone_number: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserGet(UserBase):
    id: UUID
    name: str
    email: str
    phone_number: str
    tenant_id:UUID

    class Config:
        from_attributes = True

class UserLoginResponse():
    access_token: Optional[str]
    token_type: Optional[str]
    user: UserBase

    class Config:
        from_attributes = True

class UserDelete(UserBase):
    id: UUID  




