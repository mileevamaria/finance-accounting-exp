from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import (
    CurrentUserDep,
    TransactionServiceDep,
)
from app.schemas.transactions import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter(
    prefix='/companies/{company_id}/accounts/{account_id}/transactions',
    tags=['Transactions'],
)


@router.post('', response_model=TransactionResponse)
async def create_transaction(
    company_id: UUID,
    account_id: UUID,
    data: TransactionCreate,
    current_user: CurrentUserDep,
    service: TransactionServiceDep,
):
    transaction = await service.create(
        company_id=company_id,
        account_id=account_id,
        owner_id=current_user.id,
        data=data,
    )

    return TransactionResponse.model_validate(transaction)


@router.get('', response_model=list[TransactionResponse])
async def get_transactions(
    company_id: UUID,
    account_id: UUID,
    current_user: CurrentUserDep,
    service: TransactionServiceDep,
):
    transactions = await service.get_all(
        company_id=company_id,
        account_id=account_id,
        owner_id=current_user.id,
    )

    return [
        TransactionResponse.model_validate(transaction)
        for transaction in transactions
    ]


@router.get(
    '/{transaction_id}',
    response_model=TransactionResponse,
)
async def get_transaction(
    company_id: UUID,
    account_id: UUID,
    transaction_id: UUID,
    current_user: CurrentUserDep,
    service: TransactionServiceDep,
):
    transaction = await service.get(
        transaction_id=transaction_id,
        company_id=company_id,
        account_id=account_id,
        owner_id=current_user.id,
    )

    return TransactionResponse.model_validate(transaction)


@router.patch(
    '/{transaction_id}',
    response_model=TransactionResponse,
)
async def update_transaction(
    company_id: UUID,
    account_id: UUID,
    transaction_id: UUID,
    data: TransactionUpdate,
    current_user: CurrentUserDep,
    service: TransactionServiceDep,
):
    transaction = await service.update(
        transaction_id=transaction_id,
        company_id=company_id,
        account_id=account_id,
        owner_id=current_user.id,
        data=data,
    )

    return TransactionResponse.model_validate(transaction)


@router.delete('/{transaction_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    service: TransactionServiceDep,
):
    await service.delete(transaction_id)
