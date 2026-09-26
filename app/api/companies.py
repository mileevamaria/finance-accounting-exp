from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import CompanyServiceDep, CurrentUserDep
from app.schemas.companies import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)

router = APIRouter(
    prefix='/companies',
    tags=['Companies'],
)


@router.post('', response_model=CompanyResponse)
async def create_company(
    data: CompanyCreate,
    current_user: CurrentUserDep,
    service: CompanyServiceDep,
):
    company = await service.create(current_user.id, data)
    return CompanyResponse.model_validate(company)


@router.get('', response_model=list[CompanyResponse])
async def get_my_companies(
    current_user: CurrentUserDep,
    service: CompanyServiceDep,
):
    companies = await service.get_my_companies(current_user.id)
    return [
        CompanyResponse.model_validate(company)
        for company in companies
    ]

@router.get('/{company_id}', response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    current_user: CurrentUserDep,
    service: CompanyServiceDep,
):
    company = await service.get_company(company_id, current_user.id)
    return CompanyResponse.model_validate(company)


@router.patch('/{company_id}', response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    data: CompanyUpdate,
    service: CompanyServiceDep,
):
    company = await service.update(company_id, data)
    return CompanyResponse.model_validate(company)


@router.delete('/{company_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    service: CompanyServiceDep,
):
    await service.delete(company_id)
