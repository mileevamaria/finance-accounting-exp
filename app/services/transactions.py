from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Transaction
from app.repositories import CategoryRepository, TransactionRepository
from app.schemas.transactions import (
    TransactionCreate,
    TransactionUpdate,
)
from app.services import AccountService


class TransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        category_repo: CategoryRepository,
        account_service: AccountService,
    ):
        self.transaction_repo = transaction_repo
        self.category_repo = category_repo
        self.account_service = account_service

    async def create(
        self,
        company_id: UUID,
        account_id: UUID,
        owner_id: UUID,
        data: TransactionCreate,
    ) -> Transaction:
        account = await self.account_service.get_account(
            account_id=account_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        category = await self.category_repo.get_by_id(data.category_id)

        if category is None or category.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        transaction = Transaction(
            account_id=account.id,
            category_id=category.id,
            amount=data.amount,
            occurred_at=data.occurred_at,
            counterparty=data.counterparty,
            description=data.description,
        )

        return await self.transaction_repo.create(transaction)

    async def get_all(
        self,
        company_id: UUID,
        account_id: UUID,
        owner_id: UUID,
    ) -> Sequence[Transaction]:
        await self.account_service.get_account(
            account_id=account_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        return await self.transaction_repo.get_by_account(account_id)

    async def get(
        self,
        transaction_id: UUID,
        company_id: UUID,
        account_id: UUID,
        owner_id: UUID,
    ) -> Transaction:
        await self.account_service.get_account(
            account_id=account_id,
            company_id=company_id,
            owner_id=owner_id,
        )

        transaction = await self.transaction_repo.get_by_id(transaction_id)

        if transaction is None or transaction.account_id != account_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )

        return transaction

    async def update(
        self,
        transaction_id: UUID,
        company_id: UUID,
        account_id: UUID,
        owner_id: UUID,
        data: TransactionUpdate,
    ) -> Transaction:
        transaction = await self.get(
            transaction_id=transaction_id,
            company_id=company_id,
            account_id=account_id,
            owner_id=owner_id,
        )

        if data.category_id is not None:
            category = await self.category_repo.get_by_id(data.category_id)

            if category is None or category.company_id != company_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

            transaction.category_id = category.id

        update_data = data.model_dump(
            exclude_unset=True,
            exclude={"category_id"},
        )

        for field, value in update_data.items():
            setattr(transaction, field, value)

        return await self.transaction_repo.update(transaction)

    async def delete(self, obj_id: UUID) -> None:
        await self.transaction_repo.delete(obj_id)
