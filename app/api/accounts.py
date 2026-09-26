from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import (
    AccountServiceDep,
    CurrentUserDep,
)
from app.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
)

router = APIRouter(
    prefix='/companies/{company_id}/accounts',
    tags=['Accounts'],
)


@router.post('', response_model=AccountResponse)
async def create_account(
    company_id: UUID,
    data: AccountCreate,
    current_user: CurrentUserDep,
    service: AccountServiceDep,
):
    account = await service.create(
        current_user.id,
        company_id,
        data,
    )

    return AccountResponse.model_validate(account)


@router.get('', response_model=list[AccountResponse])
async def get_accounts(
    company_id: UUID,
    current_user: CurrentUserDep,
    service: AccountServiceDep,
):
    accounts = await service.get_company_accounts(
        current_user.id,
        company_id,
    )

    return [
        AccountResponse.model_validate(account)
        for account in accounts
    ]


@router.get('/{account_id}', response_model=AccountResponse)
async def get_account(
    company_id: UUID,
    account_id: UUID,
    current_user: CurrentUserDep,
    service: AccountServiceDep,
):
    account = await service.get_account(
        current_user.id,
        company_id,
        account_id,
    )

    return AccountResponse.model_validate(account)


@router.patch('/{account_id}', response_model=AccountResponse)
async def update_account(
    company_id: UUID,
    account_id: UUID,
    data: AccountUpdate,
    current_user: CurrentUserDep,
    service: AccountServiceDep,
):
    account = await service.update(
        current_user.id,
        company_id,
        account_id,
        data,
    )

    return AccountResponse.model_validate(account)


@router.delete('{account_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    service: AccountServiceDep,
):
    await service.delete(category_id)
