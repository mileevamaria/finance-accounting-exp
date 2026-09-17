from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.core import settings


def create_access_token(user_id: UUID) -> str:
    payload = {
        'sub': str(user_id),
        'type': 'access',
        'exp': datetime.now(UTC)
        + timedelta(minutes=settings.access_token_expire_minutes),
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.token_algorithm,
    )


def create_refresh_token(
    user_id: UUID, 
    token_id: UUID,
) -> tuple[str, datetime]:
    expired_at = datetime.now(UTC) \
        + timedelta(days=settings.refresh_token_expire_days)
    payload = {
        'sub': str(user_id),
        'jti': str(token_id),
        'type': 'refresh',
        'exp': expired_at,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.token_algorithm,
    ), expired_at


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.token_algorithm],
    )
