from typing import List
from pydantic import BaseModel

from app.api.orders.db_models.order import Order
from app.api.orders.schemas.order import OrderBase



class AnanlyticResponse(BaseModel):
    total_orders:int
    total_customers:int
    total_products: int
    total_profit:float
    recent_orders:List[OrderBase]