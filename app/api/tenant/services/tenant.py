from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Tenant
from ..v1.request.tenant import CreateTenantRequest, UpdateTenantRequest
from uuid import uuid4
from datetime import datetime


class TenantService:
    @staticmethod
    def create_tenant(db: Session, tenant_request: CreateTenantRequest):
        _tenant = Tenant(
            tenant_id=uuid4(),
            company_name=tenant_request.company_name,
            email=tenant_request.email,
            phone=tenant_request.phone,
            slug=tenant_request.slug,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(_tenant)
        db.commit()
        db.refresh(_tenant)
        return _tenant

    @staticmethod
    def update_tenant(db: Session, tenant_id: str, tenant_request: UpdateTenantRequest):
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Update only provided fields
        if tenant_request.email is not None:
            tenant.email = tenant_request.email
        if tenant_request.phone is not None:
            tenant.phone = tenant_request.phone
        if tenant_request.slug is not None:
            tenant.slug = tenant_request.slug
        tenant.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(tenant)
        return tenant

    @staticmethod
    def get_tenant_by_id(db: Session, tenant_id: str):
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant

    @staticmethod
    def get_all_tenants(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Tenant).offset(skip).limit(limit).all()

    @staticmethod
    def delete_tenant(db: Session, tenant_id: str):
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        db.delete(tenant)
        db.commit()
