from fastapi import APIRouter

from app.core.dependencies import (
    AuthServiceDep,
    CurrentUserDep,
    UserServiceDep,
)
from app.schemas.auth import AuthUserResponse
from app.schemas.users import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/me', response_model=UserResponse)
async def get_user(current_user: CurrentUserDep):
    return UserResponse.model_validate(current_user)


@router.post('/', response_model=AuthUserResponse)
async def create_user(
    data: UserCreate,
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
):
    user = await user_service.create(data)
    access_token, refresh_token = await auth_service.create_tokens(user.id)
    return AuthUserResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.patch('/me', response_model=UserResponse)
async def update_user(
    data: UserUpdate,
    current_user: CurrentUserDep,
    service: UserServiceDep,
):
    user = await service.update(current_user.id, data)
    return UserResponse.model_validate(user)


@router.delete('/me', status_code=204)
async def delete_user(
    current_user: CurrentUserDep,
    service: UserServiceDep,
):
    await service.delete(current_user.id)
