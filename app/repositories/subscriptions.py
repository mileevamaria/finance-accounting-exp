from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Subscription
from app.repositories import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user(
        self,
        user_id: UUID,
    ) -> Subscription | None:
        result = await self.session.execute(
            select(Subscription).where(
                Subscription.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user_for_update(
        self,
        user_id: UUID,
    ) -> Subscription | None:
        result = await self.session.execute(
            select(Subscription)
            .where(Subscription.user_id == user_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def exists_payment(self, payment_id: str) -> bool:
        result = await self.session.execute(
            select(Subscription.id).where(
                Subscription.provider_payment_id == payment_id
            )
        )
        return result.scalar_one_or_none() is not None
