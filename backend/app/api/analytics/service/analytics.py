from sqlalchemy import select, func, and_, extract
from app.api.analytics.schemas.analytics import AnanlyticResponse
from app.api.orders.db_models.customer import Customer
from app.api.orders.db_models.order import Order
from app.api.orders.schemas.order import OrderBase
from app.api.product.db_models.product import Product
from sqlalchemy.orm import Session
import datetime

class AnalyticService:
    
    def get_analytics_dashboard(self, tenant_id: str, db: Session) -> AnanlyticResponse:
        query_total_products = select(func.count(Product.id)).where(Product.tenant_id == tenant_id)
        query_total_orders = select(func.count(Order.id)).where(Order.tenant_id == tenant_id)
        query_total_unpaid_orders = select(func.count(Order.id)).where(and_(Order.tenant_id==tenant_id,Order.status!='Paid'))
        query_total_monthly_revenue = select(func.sum(Order.order_value)).where(and_(Order.tenant_id==tenant_id,extract("month", Order.created_at)
                == datetime.datetime.now().strftime("%m")))
        query_total_received_value = select(func.sum(Order.amount_received)).where(Order.tenant_id==tenant_id)
        query_total_customers = select(func.count(Customer.id)).where(Customer.tenant_id == tenant_id)
        query_recent_orders = select(Order).where(Order.tenant_id == tenant_id).order_by(Order.created_at.desc()).limit(7)
        query_remaining_money = select(func.sum(Order.order_value-Order.amount_received)).where(Order.tenant_id==tenant_id)
        
        total_products = db.execute(query_total_products).scalar()
        total_orders = db.execute(query_total_orders).scalar()
        total_customers = db.execute(query_total_customers).scalar()
        recent_orders = db.execute(query_recent_orders).all()
        unpaid_orders = db.execute(query_total_unpaid_orders).scalar()
        monthly_revenue = db.execute(query_total_monthly_revenue).scalar()
        received_money = db.execute(query_total_received_value).scalar()
        remaining_money = db.execute(query_remaining_money).scalar()
        # Unpack tuples and convert orders to Pydantic models
        recent_orders_models = [OrderBase.from_orm(order[0]) for order in recent_orders]
        
        print(f"Total customers: {total_customers}")
        print(f"Total orders: {total_orders}")
        print(f"Total products: {total_products}")
        print(f"Total recent orders: {recent_orders}")
        
        return AnanlyticResponse(
            total_customers=total_customers,
            total_orders=total_orders,
            total_products=total_products,
            total_profit=0.0,
            unpaid_orders=unpaid_orders,
            monthly_revenue=monthly_revenue,
            received_money=received_money,
            remaining_money=remaining_money,
            recent_orders=[order.model_dump() for order in recent_orders_models]
        )
            
        