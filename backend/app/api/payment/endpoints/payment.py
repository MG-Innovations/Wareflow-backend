from app.api.payment.schemas.payment import (
    Payment,
    PaymentDelete,
    PaymentGet,
    PaymentGetResponse,
    PaymentUpdate,
)
from app.core import security
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.core.jwt import JWTBearer
from app.core.api_response import ApiResponse
from app.core import security
from app.api.payment.services.payment import payment_service
from app.api.orders.db_models.order import Order
from app.api.orders.services.customer import customer

router = APIRouter(prefix="/payment")


# Company Endpoints
@router.post("/payment", dependencies=[Depends(JWTBearer())])
def create_payment(
    payment: Payment,
    db: Session = Depends(get_db),
    auth_token: str = Depends(JWTBearer()),
):
    try:
        token = auth_token

        payload = security.decode_access_token(token)
        # Extract the UUID of the tenant
        user_id = payload.get("user_id")

        tenant_id = payload.get("tenant_id")

        new_payment = payment_service.create_payment(db, payment, user_id, tenant_id)
        return ApiResponse.response_created(
            data=Payment.model_validate(new_payment).model_dump()
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/payment/{payment_id}", dependencies=[Depends(JWTBearer())])
def get_payment(payment_id: UUID, db: Session = Depends(get_db)):
    try:
        payment = payment_service.get_payment_by_id(db, payment_id)
        if payment:
            return ApiResponse.response_ok(
                data=PaymentGetResponse.model_validate(payment).model_dump()
            )
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/payment", dependencies=[Depends(JWTBearer())])
def get_all_payments(db: Session = Depends(get_db)):
    try:
        payments = payment_service.get_payments(db)
        return ApiResponse.response_ok(
            data=[
                PaymentGetResponse.model_validate(payment).model_dump()
                for payment in payments
            ]
        )
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.delete("/payment/{payment_id}", dependencies=[Depends(JWTBearer())])
def delete_payment(payment_id: UUID, db: Session = Depends(get_db)):
    try:
        payment = payment_service.get_payment_by_id(db, payment_id)
        if payment:
            result = payment_service.delete_payment(db, payment_id)
            return ApiResponse.response_ok(data=result)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/payment/tenant/{tenant_id}", dependencies=[Depends(JWTBearer())])
def get_all_payments_for_tenant(tenant_id: UUID, db: Session = Depends(get_db)):
    try:
        payments = payment_service.get_all_payment_by_tenant_id(db, tenant_id)
        
        # Fetch all relevant orders
        order_ids = {payment.order_id for payment in payments}
        orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
        order_map = {order.id: order for order in orders}

        payment_responses = []
        for payment in payments:
            order = order_map.get(payment.order_id)
            customer_name = None
            
            if order:
                customer_id = order.customer_id
                # Fetch the customer name using the customer_id
                base_customer = customer.get(db, customer_id)
                if base_customer:
                    customer_name = base_customer.name  # Assuming 'name' is the field for customer name
            
            payment_response = PaymentGetResponse(
                id=payment.id,
                amount_paid=payment.amount_paid,
                payment_type=payment.payment_type,
                tenant_id=payment.tenant_id,
                order_id=payment.order_id,
                user_id=payment.user_id,
                description=payment.description,
                customer_name=customer_name  # Set customer_name here
            )
            payment_responses.append(payment_response.model_dump())
        
        if payments:
            return ApiResponse.response_ok(data=payment_responses)
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))


@router.get("/payment/order/{order_id}", dependencies=[Depends(JWTBearer())])
def get_all_payments_for_order(
    order_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)
):
    try:
        payments = payment_service.get_all_payment_by_order_id(db, order_id, tenant_id)
        if payments:
            return ApiResponse.response_ok(
                data=[
                    PaymentGetResponse.model_validate(payment).model_dump()
                    for payment in payments
                ]
            )
        return ApiResponse.response_not_found()
    except HTTPException as e:
        return ApiResponse.response_bad_request(status=e.status_code, message=e.detail)
    except Exception as e:
        return ApiResponse.response_internal_server_error(message=str(e))
