from fastapi import APIRouter
from app.api.auth.endpoints import tenant, user
api_router = APIRouter()

api_router.include_router(user.router,tags=["user"])
api_router.include_router(tenant.router,tags=["tenant"])