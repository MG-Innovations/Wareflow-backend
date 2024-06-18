from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union
from app.core import security
from app.api.auth.models.user import User
from app.api.auth.schemas.signup import UserSignupSchema
class CRUDUser():

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db,email=email)
        if not user:
            return None;
        if not security.verify_password(password, user.password):
            return None
        return user

    def create_user(self,db:Session,schema:UserSignupSchema)->Optional[User]:
        user = User(email=schema.email,
                    name=schema.name,
                    password=security.get_password_hash(schema.password),
                    tenant_id=schema.tenant_id,
                    phone_number=schema.phone_number)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
user = CRUDUser()

