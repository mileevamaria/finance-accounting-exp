from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.security import (
    DUMMY_HASH,
    hash_refresh_token,
    verify_password,
    verify_refresh_token,
)
from app.core.validators import is_identifier_email
from app.models import Token, User
from app.repositories import TokenRepository, UserRepository
from app.schemas.auth import AuthUser, TokenRefresh


InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid credentials',
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid refresh token',
)

class AuthService:
    def __init__(self, 
        token_repo: TokenRepository,
        user_repo: UserRepository
    ):
        self.token_repo = token_repo
        self.user_repo = user_repo

    async def create_tokens(self, user_id: UUID) -> tuple[str, str]:
        access_token = create_access_token(user_id)
        token_id = uuid4()
        refresh_token, expires_at = create_refresh_token(user_id, token_id)
        await self.token_repo.create(
            Token(
                id=token_id,
                user_id=user_id,
                token_hash=hash_refresh_token(refresh_token),
                expires_at=expires_at,
            )
        )
        return access_token, refresh_token

    async def login(self, data: AuthUser) -> tuple[User, str, str]:
        identifier = data.identifier
        if is_identifier_email(identifier):
            user = await self.user_repo.get_by_email(identifier)
        else:
            user = await self.user_repo.get_by_phone(identifier)
        if user is None:
            verify_password(data.password, DUMMY_HASH)
            raise InvalidCredentialsException

        password = data.password
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException

        access_token, refresh_token = await self.create_tokens(user.id)
        return user, access_token, refresh_token

    async def refresh_token(
        self, 
        data: TokenRefresh,
    ) -> tuple[User, str, str]:
        payload = decode_token(data.refresh_token)
        if payload['type'] != 'refresh':
            raise InvalidTokenException

        user_id = UUID(payload['sub'])
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        token_id = UUID(payload['jti'])
        stored = await self.token_repo.get_active_by_id(token_id)
        if stored is None:
            raise InvalidTokenException

        if not verify_refresh_token(
            data.refresh_token,
            stored.token_hash,
        ):
            raise InvalidTokenException
        
        await self.token_repo.revoke(stored)

        token_id = uuid4()
        new_refresh, expires_at = create_refresh_token(user_id, token_id)
        await self.token_repo.create(
            Token(
                id=token_id,
                user_id=user_id,
                token_hash=hash_refresh_token(new_refresh),
                expires_at=expires_at,
            )
        )
        access_token = create_access_token(user_id)
        return user, access_token, new_refresh

    async def logout(
        self,
        data: TokenRefresh,
    ) -> None:
        payload = decode_token(data.refresh_token)

        if payload['type'] != 'refresh':
            raise InvalidTokenException

        token = await self.token_repo.get_by_id(UUID(payload['jti']))
        if token is None:
            return

        if not verify_refresh_token(
            data.refresh_token,
            token.token_hash,
        ):
            raise InvalidTokenException

        await self.token_repo.revoke(token)


    async def logout_all(self, user_id: UUID) -> None:
        await self.token_repo.revoke_all(user_id)
