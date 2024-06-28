from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True


class CompanyGet(BaseModel):
    id: UUID  # I want UUID


class CompanyGetResponse(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True


class CompanyDelete(BaseModel):
    id: UUID  # I want UUID here
