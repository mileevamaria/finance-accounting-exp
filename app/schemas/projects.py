from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(
        default=None,
        max_length=500,
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )


class ProjectResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
