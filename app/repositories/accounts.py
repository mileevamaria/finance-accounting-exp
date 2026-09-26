from collections.abc import Sequence
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account, Transaction
from app.repositories import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Account)

    async def get_with_balance(self, account_id: UUID):
        query = (
            select(
                Account,
                (
                    Account.opening_balance +
                    func.coalesce(func.sum(Transaction.amount), Decimal('0.00'))
                ).label('balance'),
            )
            .outerjoin(
                Transaction,
                Transaction.account_id == Account.id,
            )
            .where(Account.id == account_id)
            .group_by(Account.id)
        )
        result = await self.session.execute(query)
        row = result.one_or_none()
        if row is None:
            return None

        account, balance = row
        return account, balance

    async def get_with_balances(self, company_id: UUID):
        query = (
            select(
                Account,
                (
                    Account.opening_balance +
                    func.coalesce(func.sum(Transaction.amount), Decimal('0.00'))
                ).label('balance'),
            )
            .outerjoin(
                Transaction,
                Transaction.account_id == Account.id,
            )
            .where(Account.company_id == company_id)
            .group_by(Account.id)
            .order_by(Account.name)
        )

        result = await self.session.execute(query)

        return result.all()
