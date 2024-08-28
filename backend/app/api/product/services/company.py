from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.product.db_models.company import Company
from app.api.product.schemas.company import (
    CompanyBase,
)


class CompanyService:
    def create_company(self, db: Session, company: CompanyBase) -> Company:
        db_company = Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company

    def get_company_by_id(self, db: Session, company_id: UUID) -> Optional[Company]:
        return db.query(Company).filter(Company.id == company_id).first()

    def get_companies(self, db: Session,query:str) -> List[Company]:
        return db.query(Company).where(Company.name.like(f"%{query}%")).limit(40).all()

    def delete_company(self, db: Session, company_id: UUID) -> Optional[UUID]:
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            db.delete(company)
            db.commit()
            return company_id
        return None


company_service = CompanyService()
