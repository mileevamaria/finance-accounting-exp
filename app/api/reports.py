from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import CurrentUserDep, ReportServiceDep
from app.schemas.reports import (
    CashFlowResponse,
    PnlCategoryResponse,
    PnlGroupResponse,
    PnlProjectResponse,
)

router = APIRouter(
    prefix='/companies/{company_id}/reports',
    tags=['Reports'],
)


@router.get(
    '/pnl/categories',
    response_model=list[PnlCategoryResponse],
)
async def pnl_by_categories(
    company_id: UUID,
    start: Annotated[datetime, Query(description='Начало периода')],
    end: Annotated[datetime, Query(description='Конец периода')],
    current_user: CurrentUserDep,
    service: ReportServiceDep,
):
    return await service.pnl_by_categories(
        company_id=company_id,
        owner_id=current_user.id,
        start=start,
        end=end,
    )


@router.get(
    '/pnl/groups',
    response_model=list[PnlGroupResponse],
)
async def pnl_by_groups(
    company_id: UUID,
    start: Annotated[datetime, Query(description='Начало периода')],
    end: Annotated[datetime, Query(description='Конец периода')],
    current_user: CurrentUserDep,
    service: ReportServiceDep,
):
    return await service.pnl_by_groups(
        company_id=company_id,
        owner_id=current_user.id,
        start=start,
        end=end,
    )


@router.get(
    '/pnl/projects',
    response_model=list[PnlProjectResponse],
)
async def pnl_by_projects(
    company_id: UUID,
    start: Annotated[datetime, Query(description='Начало периода')],
    end: Annotated[datetime, Query(description='Конец периода')],
    current_user: CurrentUserDep,
    service: ReportServiceDep,
):
    return await service.pnl_by_projects(
        company_id=company_id,
        owner_id=current_user.id,
        start=start,
        end=end,
    )


@router.get(
    "/cash-flow",
    response_model=list[CashFlowResponse],
)
async def cash_flow(
    company_id: UUID,
    start: Annotated[datetime, Query(description='Начало периода')],
    end: Annotated[datetime, Query(description='Конец периода')],
    current_user: CurrentUserDep,
    service: ReportServiceDep,
):
    return await service.cash_flow(
        company_id=company_id,
        owner_id=current_user.id,
        start=start,
        end=end,
    )
