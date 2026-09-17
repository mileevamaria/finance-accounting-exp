from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mixins import SoftDeleteMixin


class SoftDeletionMixin[Model: SoftDeleteMixin]:
    session: AsyncSession
    model: type[Model]

    async def get_by_id(self, obj_id: UUID) -> Model | None:
        query = (
            select(self.model)
            .where(
                self.model.id == obj_id,
                self.model.deleted_at.is_(None),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, obj_id: UUID) -> bool:
        obj = await self.get_by_id(obj_id)
        if obj:
            obj.deleted_at = datetime.now(UTC)
            await self.session.commit()
            return True
        return False
