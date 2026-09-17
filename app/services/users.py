from uuid import UUID

from fastapi import HTTPException

from app.core.security import hash_password
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def _get_user_from_db(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(obj_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        return user

    async def get(self, user_id: UUID) -> User:
        return await self._get_user_from_db(user_id=user_id)

    async def create(self, data: UserCreate) -> User:
        user_data = data.model_dump(exclude={"password"})
        user_data['hashed_password'] = hash_password(data.password)
        return await self.repo.create(User(**user_data))

    async def update(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self._get_user_from_db(user_id=user_id)
        update_data = data.model_dump(exclude_unset=True)
        if 'email' in update_data:
            existing_user = await self.repo.get_by_email(update_data['email'])
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=400, detail="Email already exists")

        for field, value in update_data.items():
            setattr(user, field, value)

        return await self.repo.update(user)

    async def delete(self, user_id: UUID) -> None:
        await self.repo.delete(user_id)
