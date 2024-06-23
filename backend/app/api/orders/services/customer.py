from uuid import UUID
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union
from app.api.orders.db_models.customer import Customer
from app.api.orders.schemas.customer import CustomerCreateInDb 
from core import security
class CustomerService:

    def get(self, db: Session,customer_id: UUID) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    def get_all(self, db:Session)->List[Customer]:
        return db.query(Customer).all();

    def create(self,db:Session,schema:CustomerCreateInDb)->Optional[Customer]:
        customer = Customer(
            name=schema.name,
            phone_number=schema.phone_number,
            created_by=schema.created_by,
            updated_by=schema.updated_by,
            tenant_id=schema.tenant_id
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    
    

customer = CustomerService()
