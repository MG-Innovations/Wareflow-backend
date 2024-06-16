from sqlalchemy.orm import Session
from ..models import Tenant
from ..v1.request.tenant import CreateTenantRequest
from uuid import uuid4

class TenantService:
    def __init__(self):
        ...
    
    @staticmethod
    def create_tenant(db: Session, tenant_request: CreateTenantRequest):
        _tenant = Tenant(
            tenant_id=uuid4(),  # Assuming this needs to be generated
            company_name="Default Company Name",  # Assign a default or fetch from tenant_request if available
            email=tenant_request.email,
            phone=tenant_request.phone,
            slug=tenant_request.slug,
            logo=uuid4(),  # Assuming this is a new logo UUID, change as needed
            created_at=tenant_request.created_at,
            updated_at=tenant_request.updated_at
        )
        print(_tenant)
        db.add(_tenant)
        db.commit()
        db.refresh(_tenant)
        return _tenant
