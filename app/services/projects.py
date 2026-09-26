from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Project
from app.repositories import CompanyRepository, ProjectRepository
from app.schemas.projects import (
    ProjectCreate,
    ProjectUpdate,
)
from app.services import CompanyService


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        company_repo: CompanyRepository,
        company_service: CompanyService,
    ):
        self.project_repo = project_repo
        self.company_repo = company_repo
        self.company_service = company_service

    async def create(
        self,
        company_id: UUID,
        owner_id: UUID,
        data: ProjectCreate,
    ) -> Project:
        await self.company_service.get_company_or_404(company_id, owner_id)

        project = Project(
            company_id=company_id,
            **data.model_dump(),
        )

        return await self.project_repo.create(project)

    async def get_all(
        self,
        company_id: UUID,
        owner_id: UUID,
    ) -> Sequence[Project]:
        await self.company_service.get_company_or_404(company_id, owner_id)

        return await self.project_repo.get_by_company(company_id)

    async def get(
        self,
        project_id: UUID,
        company_id: UUID,
        owner_id: UUID,
    ) -> Project:
        await self.company_service.get_company_or_404(company_id, owner_id)

        project = await self.project_repo.get_by_id(project_id)

        if project is None or project.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    async def update(
        self,
        project_id: UUID,
        company_id: UUID,
        owner_id: UUID,
        data: ProjectUpdate,
    ) -> Project:
        project = await self.get(
            project_id=project_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        return await self.project_repo.update(project)

    async def delete(
        self, 
        project_id: UUID,
        company_id: UUID,
        owner_id: UUID,
    ) -> None:
        project = await self.get(
            project_id=project_id,
            company_id=company_id,
            owner_id=owner_id,
        )
        await self.project_repo.delete(project.id)
