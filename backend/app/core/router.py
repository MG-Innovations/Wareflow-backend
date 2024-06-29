from fastapi import APIRouter
from app.api.auth.endpoints import tenant, user
from app.api.product.endpoints import product
from app.api.payment.endpoints import payment
from app.api.orders.endpoints import order
from app.api.orders.endpoints import customer
from app.api.product.endpoints import company
from app.api.product.endpoints import product_type
from app.api.transactions.endpoints import weekly

api_router = APIRouter()

api_router.include_router(user.router, tags=["user"])
api_router.include_router(tenant.router, tags=["tenant"])
api_router.include_router(company.router, tags=["company"])
api_router.include_router(product_type.router, tags=["product_type"])
api_router.include_router(product.router, tags=["product"])
api_router.include_router(order.router, tags=["order"])
api_router.include_router(customer.router, tags=["customer"])
api_router.include_router(payment.router, tags=["payment"])
api_router.include_router(weekly.router, tags=["weekly transactions"])

