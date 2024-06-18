from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class TenantBase(BaseModel):
    name: str
    email: str
    phone_number: str
    logo:Optional[str]
    password: str

class TenantLogin(TenantBase):
    email: str
    password: str
    
class TenantCreate(TenantBase):
    name: str
    email: str
    phone_number: str
    password: str
    logo:Optional[str]

class TenantDelete(TenantBase):
    id: UUID  #I want UUID here




