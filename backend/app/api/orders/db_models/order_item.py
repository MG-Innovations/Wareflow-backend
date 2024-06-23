
from sqlalchemy import Column, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
from sqlalchemy.sql import func

class OrderItem(Base):
    __tablename__ = "Order_Item"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4,)
    product_id = Column(UUID,ForeignKey("Product.id"),nullable=False)
    order_id = Column(UUID,ForeignKey("Order.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
    tenant_id = Column(UUID,ForeignKey('Tenant.id'),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    

    # Relationship
    order = relationship("Order", back_populates="order_items")

