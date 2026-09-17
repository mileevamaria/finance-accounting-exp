from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class _UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str | None = Field(min_length=1, max_length=64)
    email: EmailStr
    phone: str | None = Field(max_length=64)


class UserCreate(_UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)
    email: EmailStr | None = None
    phone: str | None = None

    
class UserResponse(_UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
