from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Project)

    async def get_by_company(
        self,
        company_id: UUID,
    ) -> Sequence[Project]:
        result = await self.session.execute(
            select(Project)
            .where(Project.company_id == company_id)
            .order_by(Project.name)
        )

        return result.scalars().all()
