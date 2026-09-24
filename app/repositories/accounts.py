from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account
from app.repositories import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Account)

    async def get_by_company(self, company_id: UUID) -> Sequence[Account]:
        result = await self.session.execute(
            select(Account).where(
                Account.company_id == company_id,
            )
        )
        return result.scalars().all()
