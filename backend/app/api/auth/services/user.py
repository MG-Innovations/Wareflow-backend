from uuid import UUID
from app.core.logging import logger
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union
from app.core import security
from app.api.auth.db_models.user import User
from app.api.auth.schemas.user import UserCreate
class UserService():

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db,email=email)
        if not user:
            return None;
        if not security.verify_password(password, user.password):
            return None
        return user

    def create_user(self,db:Session,schema:UserCreate)->Optional[User]:
        user = User(email=schema.email,
                    name=schema.name,
                    password=security.get_password_hash(schema.password),
                    phone_number=schema.phone_number,
                    tenant_id=schema.tenant_id,)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user(self, db:Session, id: UUID)->Optional[User]:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            return None
        return user
    
user = UserService()

