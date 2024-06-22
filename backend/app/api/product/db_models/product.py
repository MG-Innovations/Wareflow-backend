
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = "Product"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4,)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    buying_price = Column(Float, nullable=False)
    selling_price = Column(Float,nullable=False)
    image = Column(String,nullable=True)
    stock = Column(Integer,nullable=False)
    tenant_id = Column(UUID,ForeignKey('Tenant.id'),nullable=False)
    company_id = Column(UUID, ForeignKey('Company.id'),nullable=False)
    product_type_id = Column(UUID, ForeignKey('ProductType.id'),nullable=False)
    created_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    updated_by = Column(UUID, ForeignKey('User.id'),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    

    # Relationship
    company = relationship("Company", back_populates="products")
    product_type = relationship("ProductType", back_populates="products")
    created_by = relationship("User", back_populates="created_products")
    updated_by = relationship("User", back_populates="updated_products")
