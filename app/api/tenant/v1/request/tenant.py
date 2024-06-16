from typing import List, Optional, Union
from datetime import datetime
from pydantic import BaseModel , validator
from typing_extensions import Literal

class CreateTenantRequest(BaseModel):
    email: str
    phone: Optional[str]
    slug: Optional[str]
    logo: Optional[str]
    created_at: Optional[str]  # ISO 8601 datetime string
    updated_at: Optional[str]  # ISO 8601 datetime string
    company_name: Optional[str]  # Add this if needed

class UpdateTenantRequest(BaseModel):
    tenant_id: str
    email: str
    phone: Optional[str]
    slug: Optional[str]
    logo: Optional[str]
    created_at: Optional[str]  # ISO 8601 datetime string
    updated_at: Optional[str]  # ISO 8601 datetime string

