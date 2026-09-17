from fastapi import APIRouter, status

from app.core.dependencies import AuthServiceDep, CurrentUserDep
from app.schemas.auth import (
    AuthUser,
    AuthUserResponse,
    TokenRefresh,
)
from app.schemas.users import UserResponse

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/login', response_model=AuthUserResponse)
async def login(
    data: AuthUser,
    service: AuthServiceDep,
):
    user, access_token, refresh_token = await service.login(data)
    return AuthUserResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )

@router.post('/refresh', response_model=AuthUserResponse)
async def refresh(
    data: TokenRefresh,
    service: AuthServiceDep,
):
    user, access_token, refresh_token = await service.refresh_token(data)
    return AuthUserResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    data: TokenRefresh,
    service: AuthServiceDep,
):
    await service.logout(data)


@router.post('/logout-all', status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    current_user: CurrentUserDep,
    service: AuthServiceDep,
):
    await service.logout_all(current_user.id)
