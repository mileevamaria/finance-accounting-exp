from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.subscriptions import (
    SubscriptionPlan,
    SubscriptionStatus,
)


class PaymentCreateResponse(BaseModel):
    payment_id: str
    confirmation_url: str


class SubscriptionResponse(BaseModel):
    plan: SubscriptionPlan
    status: SubscriptionStatus
    current_period_end: datetime | None


class YooKassaWebhookObject(BaseModel):
    id: str
    metadata: dict[str, str]


class YooKassaWebhook(BaseModel):
    event: str
    object: YooKassaWebhookObject
