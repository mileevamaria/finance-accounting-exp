from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PnlCategoryResponse(BaseModel):
    category_id: UUID
    category_name: str
    group_name: str
    amount: Decimal


class PnlGroupResponse(BaseModel):
    group_id: UUID
    group_name: str
    amount: Decimal


class PnlProjectResponse(BaseModel):
    project_id: UUID | None
    project_name: str
    income: Decimal
    expense: Decimal
    profit: Decimal

class CashFlowResponse(BaseModel):
    period: str
    income: Decimal
    expense: Decimal
    net: Decimal
