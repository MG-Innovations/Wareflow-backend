from sqlalchemy import Column, Integer, String

from config import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    buying_price = Column(Integer)
    selling_price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
