from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.categories import CategoryIconColor


class CategoryGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CategoryGroupUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class CategoryGroupResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    group_id: UUID
    name: str = Field(min_length=1, max_length=255)
    icon_color: CategoryIconColor = CategoryIconColor.GREY


class CategoryUpdate(BaseModel):
    group_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    icon_color: CategoryIconColor | None = None


class CategoryResponse(BaseModel):
    id: UUID
    company_id: UUID
    group_id: UUID
    name: str
    icon_color: CategoryIconColor

    model_config = ConfigDict(from_attributes=True)
