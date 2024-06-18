


from pydantic import BaseModel


class TenantSignupSchema(BaseModel):
    email:str
    name:str
    password:str
    logo:str
    phone_number:str

class UserSignupSchema(BaseModel):
    email:str
    name:str
    password:str
    tenant_id:str
    phone_number:str    
