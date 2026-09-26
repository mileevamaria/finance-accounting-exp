from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import (
    CurrentUserDep,
    ProjectServiceDep,
)
from app.schemas.projects import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(
    prefix='/companies/{company_id}/projects',
    tags=['Projects'],
)


@router.post('', response_model=ProjectResponse)
async def create_project(
    company_id: UUID,
    data: ProjectCreate,
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
):
    project = await service.create(
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return ProjectResponse.model_validate(project)


@router.get('', response_model=list[ProjectResponse])
async def get_projects(
    company_id: UUID,
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
):
    projects = await service.get_all(
        company_id=company_id,
        owner_id=current_user.id,
    )

    return [
        ProjectResponse.model_validate(project)
        for project in projects
    ]


@router.get('/{project_id}', response_model=ProjectResponse)
async def get_project(
    company_id: UUID,
    project_id: UUID,
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
):
    project = await service.get(
        project_id=project_id,
        company_id=company_id,
        owner_id=current_user.id,
    )

    return ProjectResponse.model_validate(project)


@router.patch('/{project_id}', response_model=ProjectResponse)
async def update_project(
    company_id: UUID,
    project_id: UUID,
    data: ProjectUpdate,
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
):
    project = await service.update(
        project_id=project_id,
        company_id=company_id,
        owner_id=current_user.id,
        data=data,
    )

    return ProjectResponse.model_validate(project)


@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: UUID,
    service: ProjectServiceDep,
) -> None:
    await service.delete(project_id)
