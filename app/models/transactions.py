from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import Account, Category


class Transaction(Base, UUIDMixin):
    __tablename__ = 'transactions'

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE'),
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT'),
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    occurred_at: Mapped[datetime]
    description: Mapped[str | None] = mapped_column(String(500))
    counterparty: Mapped[str | None] = mapped_column(String(255))

    account: Mapped['Account'] = relationship(
        back_populates='transactions',
    )
    category: Mapped['Category'] = relationship(
        back_populates='transactions',
    )
