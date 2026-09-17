from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories import BaseRepository, SoftDeletionMixin


class UserRepository(SoftDeletionMixin[User], BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(
            User.email == email, 
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        query = select(User).where(
            User.phone == phone,
            User.deleted_at.is_(None),
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()



