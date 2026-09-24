from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account, Transaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Transaction)

    async def get_by_account(
        self,
        account_id: UUID,
    ) -> Sequence[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.occurred_at.desc())
        )

        return result.scalars().all()

    async def get_by_period(
        self,
        account_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(
                Transaction.account_id == account_id,
                Transaction.occurred_at >= start,
                Transaction.occurred_at <= end,
            )
            .order_by(Transaction.occurred_at.desc())
        )

        return result.scalars().all()

    async def get_by_company(
        self,
        company_id: UUID,
    ) -> Sequence[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .join(Account)
            .where(Account.company_id == company_id)
            .order_by(Transaction.occurred_at.desc())
        )

        return result.scalars().all()
