from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Account, Company
from app.repositories import AccountRepository, CompanyRepository
from app.schemas.accounts import AccountCreate, AccountUpdate


class AccountService:
    def __init__(
        self, 
        account_repo: AccountRepository,
        company_repo: CompanyRepository,
    ):
        self.account_repo = account_repo
        self.company_repo = company_repo

    async def get_company_or_404(
        self,
        company_id: UUID,
        owner_id: UUID,
    ) -> Company:
        company = await self.company_repo.get_by_id(obj_id=company_id)
        if company is None or company.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Company not found',
            )

        return company

    async def create(
        self, 
        company_id: UUID,
        owner_id: UUID, 
        data: AccountCreate,
    ) -> Account:
        await self.get_company_or_404(company_id, owner_id)

        account = Account(company_id=company_id, **data.model_dump())
        return await self.account_repo.create(account)

    async def get_all(
        self, 
        company_id: UUID, 
        owner_id: UUID,
    ) -> list[tuple[Account, Decimal]]:
        await self.get_company_or_404(company_id, owner_id)
        accounts = await self.account_repo.get_with_balances(company_id)
        return [(account, balance) for account, balance in accounts]

    async def get(
        self, 
        account_id: UUID,
        company_id: UUID, 
        owner_id: UUID,
    ) -> tuple[Account, Decimal]:
        await self.get_company_or_404(company_id, owner_id)

        row = await self.account_repo.get_with_balance(account_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Account not found',
            )
        account, balance = row
        if account is None or account.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Account not found',
            )
        return account, balance

    async def update(
        self,
        owner_id: UUID,
        company_id: UUID,
        account_id: UUID,
        data: AccountUpdate,
    ) -> Account:
        account, _ = await self.get(
            owner_id=owner_id,
            company_id=company_id,
            account_id=account_id,
        )
        
        account_data = data.model_dump(exclude_unset=True)
        for field, value in account_data.items():
            setattr(account, field, value)
        return await self.account_repo.update(account)

    async def delete(self, obj_id: UUID) -> None:
        await self.account_repo.delete(obj_id)
