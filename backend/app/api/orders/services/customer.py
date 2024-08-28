from uuid import UUID
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union
from app.api.orders.db_models.customer import Customer
from app.api.orders.schemas.customer import CustomerCreateInDb
from core import security
from sqlalchemy import select, and_, or_


class CustomerService:

    def get(self,db: Session, customer_id: UUID) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    def get_all(
        self,
        db: Session,
        tenant_id: UUID,
        search: str = "",
    ) -> List[Customer]:
        filters = [Customer.tenant_id == tenant_id]
        filters.append(Customer.name.like(f"%{search}%"))
        stmt = (
            select(
                Customer.id,
                Customer.name,
                Customer.phone_number,
                Customer.tenant_id,
                Customer.created_by,
                Customer.updated_by,
            )
            .select_from(Customer)
            .filter(and_(*filters))
        )
        results = db.execute(stmt)
        customers = []
        for customer in results:
            data = {
                "id": customer.id,
                "name": customer.name,
                "phone_number": customer.phone_number,
                "tenant_id": customer.tenant_id,
                "created_by": customer.created_by,
                "updated_by": customer.updated_by,
            }
            customers.append(data)
        return customers

    def create(self, db: Session, schema: CustomerCreateInDb) -> Optional[Customer]:
        customer = Customer(
            name=schema.name,
            phone_number=schema.phone_number,
            created_by=schema.created_by,
            updated_by=schema.updated_by,
            tenant_id=schema.tenant_id,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer


customer = CustomerService()
