from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import (
    AccountServiceDep,
    CurrentUserDep,
)
from app.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountResponseWithBalance,
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
    accounts = await service.get_all(
        current_user.id,
        company_id,
    )

    return [
        AccountResponseWithBalance(
            id=account.id,
            company_id=account.company_id,
            name=account.name,
            type=account.type,
            currency=account.currency,
            opening_balance=account.opening_balance,
            balance=balance,
        )
        for account, balance in accounts
    ]


@router.get('/{account_id}', response_model=AccountResponse)
async def get_account(
    company_id: UUID,
    account_id: UUID,
    current_user: CurrentUserDep,
    service: AccountServiceDep,
):
    account, balance = await service.get(
        current_user.id,
        company_id,
        account_id,
    )

    return AccountResponseWithBalance(
        id=account.id,
        company_id=account.company_id,
        name=account.name,
        type=account.type,
        currency=account.currency,
        opening_balance=account.opening_balance,
        balance=balance,
    )


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
async def delete_account(
    account_id: UUID,
    service: AccountServiceDep,
):
    await service.delete(account_id)
