
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
from sqlalchemy.sql import func

class Customer(Base):
    __tablename__ = "Customer"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4,)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    tenant_id = Column(UUID,ForeignKey('Tenant.id'),nullable=False)
    created_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    updated_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    

