from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
from sqlalchemy.sql import func


class Payment(Base):
    __tablename__ = "Payment"
    id = Column(
        UUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    amount_paid = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    tenant_id = Column(UUID, ForeignKey("Tenant.id"), nullable=False)
    order_id = Column(UUID, ForeignKey("Order.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("User.id"), nullable=False)
    description = Column(String, nullable=False)
    created_by = Column(UUID, ForeignKey("User.id"), nullable=False)
    updated_by = Column(UUID, ForeignKey("User.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
