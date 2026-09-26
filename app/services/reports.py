from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from app.repositories import ReportRepository
from app.schemas.reports import (
    CashFlowResponse,
    PnlCategoryResponse,
    PnlGroupResponse,
    PnlProjectResponse,
)
from app.services import CompanyService


class ReportService:
    def __init__(
        self,
        report_repo: ReportRepository,
        company_service: CompanyService,
    ):
        self.report_repo = report_repo
        self.company_service = company_service

    async def pnl_by_categories(
        self,
        company_id: UUID,
        owner_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[PnlCategoryResponse]:
        await self.company_service.get_company_or_404(company_id, owner_id)
        rows = await self.report_repo.pnl_by_categories(
            company_id,
            start,
            end,
        )
        return [
            PnlCategoryResponse(
                category_id=row.category_id,
                category_name=row.category_name,
                group_name=row.group_name,
                amount=row.amount,
            )
            for row in rows
        ]

    async def pnl_by_groups(
        self,
        company_id: UUID,
        owner_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[PnlGroupResponse]:
        await self.company_service.get_company_or_404(
            company_id,
            owner_id,
        )
        rows = await self.report_repo.pnl_by_groups(
            company_id,
            start,
            end,
        )
        return [
            PnlGroupResponse(
                group_id=row.group_id,
                group_name=row.group_name,
                amount=row.amount,
            )
            for row in rows
        ]

    async def pnl_by_projects(
        self,
        company_id: UUID,
        owner_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[PnlProjectResponse]:
        await self.company_service.get_company_or_404(
            company_id,
            owner_id,
        )
        rows = await self.report_repo.pnl_by_projects(
            company_id,
            start,
            end,
        )
        return [
            PnlProjectResponse(
                project_id=row.project_id,
                project_name=row.project_name,
                income=row.income,
                expense=row.expense,
                profit=row.profit,
            )
            for row in rows
        ]

    async def cash_flow(
        self,
        company_id: UUID,
        owner_id: UUID,
        start: datetime,
        end: datetime,
    ) -> Sequence[CashFlowResponse]:
        await self.company_service.get_company_or_404(company_id, owner_id)
        rows = await self.report_repo.cash_flow(company_id, start, end)
        return [
            CashFlowResponse(
                period=row.period,
                income=row.income,
                expense=row.expense,
                net=row.net,
            )
            for row in rows
        ]
