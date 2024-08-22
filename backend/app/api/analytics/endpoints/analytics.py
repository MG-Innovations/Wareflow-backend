from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.api import deps
from app.api.analytics.service.analytics import AnalyticService
from app.core import security
from app.core.api_response import ApiResponse
from app.core.jwt import JWTBearer


router = APIRouter(prefix="/analytics")

@router.get("/dashboard",dependencies=[Depends(JWTBearer())])
def get_analytics_dashboard(
    db:Session=Depends(deps.get_db),
    auth_token:str=Depends(JWTBearer())
):
    try:
        token = security.decode_access_token(auth_token)
        tenant_id = token.get('tenant_id')
        result = AnalyticService().get_analytics_dashboard(
            tenant_id=tenant_id,
            db=db
        )
        return ApiResponse.response_ok(
            data=result
        )
    except Exception as e:
        print(f"Error in analytics {str(e)}")
        return ApiResponse.response_internal_server_error(message=str(e))