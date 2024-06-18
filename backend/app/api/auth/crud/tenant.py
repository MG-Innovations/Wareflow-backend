from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union
from models.tenant import Tenant

from core import security
class CRUDTenant:

    def get_by_email(self, db: Session, *, email: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[Tenant]:
        user = self.get_by_email(db,email=email)
        if not user:
            return None;
        if not security.verify_password(password, user.password):
            return None
        return user

# user = CRUDTenant(User)
