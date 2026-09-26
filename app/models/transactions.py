from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDMixin

if TYPE_CHECKING:
    from app.models import Account, Category, Project


class Transaction(Base, UUIDMixin):
    __tablename__ = 'transactions'

    __table_args__ = (
        Index('ix_transactions_account_date', 'account_id', 'occurred_at'),
        Index('ix_transactions_category', 'category_id'),
        Index('ix_transactions_project', 'project_id'),
    )


    account_id: Mapped[UUID] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE'),
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT'),
    )
    project_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('projects.id', ondelete='SET NULL'),
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

    project: Mapped['Project | None'] = relationship(
        back_populates='transactions',
    )
