from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Token
from app.repositories import BaseRepository


class TokenRepository(BaseRepository[Token]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Token)
    
    async def get_active_by_id(self, obj_id: UUID) -> Token | None:
        query = select(Token).where(
            Token.id == obj_id,
            Token.revoked_at.is_(None),
            Token.expires_at > datetime.now(UTC),
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def revoke(self, token: Token) -> Token:
        token.revoked_at = datetime.now(UTC)
        return await self.update(token)

    async def revoke_all(self, user_id: UUID) -> int:
        query = select(Token).where(
            Token.user_id == user_id,
            Token.revoked_at.is_(None),
        )

        result = await self.session.execute(query)
        tokens = result.scalars().all()

        now = datetime.now(UTC)
        for token in tokens:
            token.revoked_at = now

        await self.session.commit()
        return len(tokens)
