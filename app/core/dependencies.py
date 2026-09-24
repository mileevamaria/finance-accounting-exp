from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import decode_token
from app.db import get_session
from app.models import User
from app.repositories import (
    AccountRepository,
    CompanyRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    AccountService,
    AuthService,
    CompanyService,
    UserService,
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep) -> UserService:
    return UserService(repo=UserRepository(session))

UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(
        user_repo=UserRepository(session),
        token_repo=TokenRepository(session),
    )

AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode_token(token)
        if payload.get('type') != 'access':
            raise credentials_exception
        user_id = UUID(payload['sub'])

    except (InvalidTokenError, ValueError, KeyError):
        raise credentials_exception

    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user

CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]

def get_account_service(session: SessionDep) -> AccountService:
    return AccountService(
        account_repo=AccountRepository(session),
        company_repo=CompanyRepository(session),
    )

AccountServiceDep = Annotated[
    AccountService,
    Depends(get_account_service),
]

def get_company_service(session: SessionDep) -> CompanyService:
    return CompanyService(
        CompanyRepository(session),
    )

CompanyServiceDep = Annotated[
    CompanyService,
    Depends(get_company_service),
]
