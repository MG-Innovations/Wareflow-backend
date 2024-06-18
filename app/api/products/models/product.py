from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4

from config import Base

import datetime


class ProductType(Base):
    __tablename__ = "product_type"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    description = Column(String)


class Product(Base):
    __tablename__ = "product"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    # type_id = Column(UUID(as_uuid=True), ForeignKey("product_type.id"), nullable=False)
    buying_price = Column(Integer, default=0)
    selling_price = Column(Integer)
    # company = Column(String)
    # created_at = Column(DateTime, default=datetime.datetime.now())
    # updated_at = Column(DateTime)
    # created_by = Column(UUID(as_uuid=True), default=uuid4)
    # updated_by = Column(UUID(as_uuid=True), default=uuid4)
