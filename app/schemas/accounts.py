from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.accounts import AccountCurrency, AccountType

Money = Annotated[
    Decimal,
    Field(max_digits=15, decimal_places=2),
]


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: AccountType
    currency: AccountCurrency
    opening_balance: Money = Decimal("0.00")


class AccountUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    opening_balance: Decimal | None = None


class AccountResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    type: AccountType
    currency: AccountCurrency
    opening_balance: Money

    model_config = ConfigDict(from_attributes=True)
