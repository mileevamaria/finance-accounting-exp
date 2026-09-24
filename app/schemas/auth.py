from pydantic import BaseModel, Field

from app.schemas.users import UserResponse


class AuthUser(BaseModel):
    identifier: str
    password: str = Field(min_length=8, max_length=128)


class AuthUserResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    user: UserResponse


class TokenRefresh(BaseModel):
    refresh_token: str
