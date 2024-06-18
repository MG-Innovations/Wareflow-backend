from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union
from app.api.auth.db_models.tenant import Tenant
from app.api.auth.schemas.tenant import TenantLogin, TenantCreate
from core import security
class TenantService:

    def get_by_email(self, db: Session, *, email: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[Tenant]:
        tenant = self.get_by_email(db,email=email)
        if not tenant:
            return None;
        if not security.verify_password(password, tenant.password):
            return None
        return tenant
    
    def create_tenant(self,db:Session,schema:TenantCreate)->Optional[Tenant]:
        tenant = Tenant(email=schema.email,
                    name=schema.name,
                    logo_url=schema.logo,
                    password=security.get_password_hash(schema.password),
                    phone_number=schema.phone_number)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant

tenant = TenantService()
