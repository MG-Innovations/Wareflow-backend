from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class TenantBase(BaseModel):
    name: str
    email: str
    phone_number: str
    logo_url:Optional[str]    
class TenantCreate(TenantBase):
    name: str
    email: str
    phone_number: str
    logo_url:Optional[str]

    class Config:
        from_attributes = True

class TenantDelete(TenantBase):
    id: UUID  #I want UUID here




