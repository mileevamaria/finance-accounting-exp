from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Company
from app.repositories import BaseRepository, SoftDeletionMixin


class CompanyRepository(SoftDeletionMixin[Company], BaseRepository[Company]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Company)

    async def get_by_owner(self, owner_id: UUID) -> Sequence[Company]:
        result = await self.session.execute(
            select(Company).where(
                Company.owner_id == owner_id,
            )
        )
        return result.scalars().all()
