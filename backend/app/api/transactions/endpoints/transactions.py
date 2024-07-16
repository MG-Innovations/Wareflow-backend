from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import JWTBearer
from app.api.deps import get_db
from sqlalchemy.orm import Session
from app.core.api_response import ApiResponse
from app.api.transactions.services.transactions import TransactionsService

router = APIRouter(prefix="/transactions")


@router.get("/weekly", dependencies=[Depends(JWTBearer())])
def get_weekly_transactions(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token
        transactions_service = TransactionsService()
        refreshed_weekly_transactions = transactions_service.get_weekly_transactions(
            db, token
        )
        return ApiResponse.response_ok(data=refreshed_weekly_transactions)

    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/monthly", dependencies=[Depends(JWTBearer())])
def get_monthly_transactions(
    db: Session = Depends(get_db), auth_token: str = Depends(JWTBearer())
):
    try:
        token = auth_token
        transactions_service = TransactionsService()
        refreshed_monthly_transactions = transactions_service.get_monthly_transactions(
            db, token
        )
        return ApiResponse.response_ok(data=refreshed_monthly_transactions)

    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
