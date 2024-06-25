
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
from sqlalchemy.sql import func

class Order(Base):
    __tablename__ = "Order"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4,)
    tenant_id = Column(UUID,ForeignKey('Tenant.id'),nullable=False)
    order_value = Column(Float, nullable=False)
    amount_received = Column(Float, nullable=True, default=0.0)
    status = Column(String, nullable=True, default='Unpaid')
    customer_id = Column(UUID,ForeignKey('Customer.id'),nullable=False)
    created_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    updated_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    

    # Relationship
    order_items = relationship("OrderItem", back_populates="order")

