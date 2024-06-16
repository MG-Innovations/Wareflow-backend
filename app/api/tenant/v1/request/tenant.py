from typing import List, Optional, Union
from datetime import datetime
from pydantic import BaseModel , validator , EmailStr , Field
from typing_extensions import Literal

class CreateTenantRequest(BaseModel):
    email: str
    phone: Optional[str]
    slug: Optional[str]
    company_name: Optional[str]  # Add this if needed

class UpdateTenantRequest(BaseModel):
    email: Optional[EmailStr]
    phone: Optional[str]
    slug: Optional[str]

