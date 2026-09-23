from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class _CompanyBase(BaseModel):
    full_name: str | None = None
    description: str | None = None
    inn: str | None = None
    kpp: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class CompanyCreate(_CompanyBase):
    name: str = Field(min_length=1, max_length=255)


class CompanyUpdate(_CompanyBase):
    name: str | None = None


class CompanyResponse(_CompanyBase):
    id: UUID
    owner_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
