from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Company
from app.repositories import CompanyRepository
from app.schemas.companies import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def create(self, owner_id: UUID, data: CompanyCreate) -> Company:
        company = Company(owner_id=owner_id, **data.model_dump())
        return await self.repo.create(company)

    async def get_my_companies(self, owner_id: UUID) -> Sequence[Company]:
        return await self.repo.get_by_owner(owner_id)

    async def get_company(
        self, 
        company_id: UUID, 
        owner_id: UUID,
    ) -> Company | None:
        company = await self.repo.get_by_id(obj_id=company_id)
        if not company or company.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Company not found',
            )
        return company

    async def update(self, company_id: UUID, data: CompanyUpdate) -> Company:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Company not found',
            )
        
        company_data = data.model_dump(exclude_unset=True)
        for field, value in company_data.items():
            setattr(company, field, value)
        
        return await self.repo.update(company)

    async def delete(self, obj_id: UUID) -> None:
        await self.repo.delete(obj_id)
