from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union
from models.users import User

from app.core import security
class CRUDUser:

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db,email=email)
        if not user:
            return None;
        if not security.verify_password(password, user.password):
            return None
        return user
    
# user = CRUDUser(User)

