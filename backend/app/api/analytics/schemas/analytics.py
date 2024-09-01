from typing import List
from pydantic import BaseModel

from app.api.orders.db_models.order import Order
from app.api.orders.schemas.order import OrderBase



class AnanlyticResponse(BaseModel):
    total_orders:int
    total_customers:int
    total_products: int
    total_profit:float
    unpaid_orders: int | None
    monthly_revenue: float | None
    received_money: float | None
    remaining_money: float
    recent_orders:List[OrderBase]