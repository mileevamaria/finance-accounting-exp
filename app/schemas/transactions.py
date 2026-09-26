from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.types import Money


class TransactionCreate(BaseModel):
    amount: Money
    category_id: UUID
    occurred_at: datetime
    project_id: UUID | None = None
    counterparty: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=500)


class TransactionUpdate(BaseModel):
    amount: Money | None = None
    category_id: UUID | None = None
    project_id: UUID | None = None
    occurred_at: datetime | None = None
    counterparty: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=500)


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    category_id: UUID
    amount: Money
    occurred_at: datetime
    counterparty: str | None
    description: str | None

    model_config = ConfigDict(from_attributes=True)
