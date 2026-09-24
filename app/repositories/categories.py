from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, CategoryGroup
from app.repositories.base import BaseRepository


class CategoryGroupRepository(BaseRepository[CategoryGroup]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CategoryGroup)

    async def get_by_company(
        self,
        company_id: UUID,
    ) -> Sequence[CategoryGroup]:
        result = await self.session.execute(
            select(CategoryGroup)
            .where(CategoryGroup.company_id == company_id)
            .order_by(CategoryGroup.name)
        )

        return result.scalars().all()


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Category)

    async def get_by_company(
        self,
        company_id: UUID,
    ) -> Sequence[Category]:
        result = await self.session.execute(
            select(Category)
            .where(Category.company_id == company_id)
            .order_by(Category.name)
        )

        return result.scalars().all()

    async def get_by_group(
        self,
        group_id: UUID,
    ) -> Sequence[Category]:
        result = await self.session.execute(
            select(Category)
            .where(Category.group_id == group_id)
            .order_by(Category.name)
        )

        return result.scalars().all()
