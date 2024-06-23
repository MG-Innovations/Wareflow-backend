from fastapi import APIRouter
from app.api.auth.endpoints import tenant, user
from app.api.product.endpoints import product
from app.api.orders.endpoints import customer,order
api_router = APIRouter()

api_router.include_router(user.router,tags=["user"])
api_router.include_router(tenant.router,tags=["tenant"])
api_router.include_router(product.router,tags=["product"])
api_router.include_router(customer.router,tags=["customer"])
api_router.include_router(order.router,tags=["order"])