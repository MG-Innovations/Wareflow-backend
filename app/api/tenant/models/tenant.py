from uuid import uuid4
from sqlalchemy import Column, Unicode, DateTime
from sqlalchemy.dialects.postgresql import UUID
from config import Base


class Tenant(Base):
    __tablename__ = "tenant"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    company_name = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False)
    phone = Column(Unicode(20), nullable=True)
    slug = Column(Unicode(255), nullable=True)
    logo = Column(Unicode(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
