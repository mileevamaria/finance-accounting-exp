from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Account,
    Category,
    CategoryGroup,
    Project,
    Transaction,
)


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def pnl_by_categories(
        self,
        company_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[Row]:
        query = (
            select(
                Category.id.label('category_id'),
                Category.name.label('category_name'),
                CategoryGroup.name.label('group_name'),
                func.coalesce(
                    func.sum(Transaction.amount),
                    Decimal('0.00'),
                ).label('amount'),
            )
            .join(
                CategoryGroup,
                Category.group_id == CategoryGroup.id,
            )
            .outerjoin(
                Transaction,
                (Transaction.category_id == Category.id)
                & (Transaction.occurred_at >= start)
                & (Transaction.occurred_at <= end),
            )
            .outerjoin(
                Account,
                (Transaction.account_id == Account.id)
                & (Account.company_id == company_id),
            )
            .where(Category.company_id == company_id)
            .group_by(
                Category.id,
                Category.name,
                CategoryGroup.name,
            )
            .order_by(
                CategoryGroup.name,
                Category.name,
            )
        )

        result = await self.session.execute(query)
        return result.all()

    async def pnl_by_groups(
        self,
        company_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[Row]:
        query = (
            select(
                CategoryGroup.id.label('group_id'),
                CategoryGroup.name.label('group_name'),
                func.coalesce(
                    func.sum(Transaction.amount),
                    Decimal('0.00'),
                ).label('amount'),
            )
            .outerjoin(
                Category,
                Category.group_id == CategoryGroup.id,
            )
            .outerjoin(
                Transaction,
                (Transaction.category_id == Category.id)
                & (Transaction.occurred_at >= start)
                & (Transaction.occurred_at <= end),
            )
            .outerjoin(
                Account,
                (Transaction.account_id == Account.id)
                & (Account.company_id == company_id),
            )
            .where(CategoryGroup.company_id == company_id)
            .group_by(
                CategoryGroup.id,
                CategoryGroup.name,
            )
            .order_by(CategoryGroup.name)
        )

        result = await self.session.execute(query)
        return result.all()

    async def pnl_by_projects(
        self,
        company_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[Row]:
        income = func.coalesce(
            func.sum(
                case(
                    (Transaction.amount > 0, Transaction.amount),
                    else_=Decimal('0.00'),
                )
            ),
            Decimal('0.00'),
        )

        expense = func.coalesce(
            func.sum(
                case(
                    (Transaction.amount < 0, Transaction.amount),
                    else_=Decimal('0.00'),
                )
            ),
            Decimal('0.00'),
        )

        project_name = func.coalesce(
            Project.name,
            'Без проекта',
        )

        query = (
            select(
                Project.id.label('project_id'),
                project_name.label('project_name'),
                income.label('income'),
                expense.label('expense'),
                (income + expense).label('profit'),
            )
            .outerjoin(Project, Transaction.project_id == Project.id)
            .join(Account, Transaction.account_id == Account.id)
            .where(
                Account.company_id == company_id,
                Transaction.occurred_at >= start,
                Transaction.occurred_at <= end,
            )
            .group_by(
                Project.id,
                project_name,
            )
            .order_by(project_name)
        )

        result = await self.session.execute(query)
        return result.all()

    async def cash_flow(
        self,
        company_id: UUID,
        start: datetime,
        end: datetime,
    ):
        period = func.to_char(
            func.date_trunc('month', Transaction.occurred_at),
            'YYYY-MM',
        )

        income = func.coalesce(
            func.sum(
                case(
                    (Transaction.amount > 0, Transaction.amount),
                    else_=Decimal('0.00'),
                )
            ),
            Decimal('0.00'),
        )

        expense = func.coalesce(
            func.sum(
                case(
                    (Transaction.amount < 0, Transaction.amount),
                    else_=Decimal('0.00'),
                )
            ),
            Decimal('0.00'),
        )

        query = (
            select(
                period.label('period'),
                income.label('income'),
                expense.label('expense'),
                (income + expense).label('net'),
            )
            .join(
                Account,
                Transaction.account_id == Account.id,
            )
            .where(
                Account.company_id == company_id,
                Transaction.occurred_at >= start,
                Transaction.occurred_at <= end,
            )
            .group_by(period)
            .order_by(period)
        )

        result = await self.session.execute(query)
        return result.all()
