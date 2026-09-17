from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[Model]:
    def __init__(self, session: AsyncSession, model: type[Model]):
        self.session = session
        self.model = model

    async def get_by_id(self, obj_id: UUID) -> Model | None:
        return await self.session.get(self.model, obj_id)

    async def create(self, obj: Model) -> Model:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: Model) -> Model:
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: UUID) -> bool:
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False
