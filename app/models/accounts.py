from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import Company


class AccountCurrency(str, Enum):
    USD = 'usd'
    EUR = 'eur'
    RUB = 'rub'


class AccountType(str, Enum):
    BANK = 'bank'
    CASH = 'cash'


class Account(Base, UUIDMixin):
    __tablename__ = 'accounts'

    __table_args__ = (
        Index("ix_accounts_company", "company_id"),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey('companies.id', ondelete='CASCADE'),
    )
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType))
    currency: Mapped[AccountCurrency] = mapped_column(SQLEnum(AccountCurrency))
    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), default=Decimal('0.00'),
    )
    
    company: Mapped['Company'] = relationship(
        back_populates='accounts',
    ) 
