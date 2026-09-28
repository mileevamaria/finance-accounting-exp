from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class WebSocketEvent(StrEnum):
    TRANSACTION_CREATED = 'transaction_created'
    TRANSACTION_UPDATED = 'transaction_updated'
    TRANSACTION_DELETED = 'transaction_deleted'

    ACCOUNT_UPDATED = 'account_updated'

    PROJECT_CREATED = 'project_created'
    PROJECT_UPDATED = 'project_updated'

    CATEGORY_UPDATED = 'category_updated'

    SUBSCRIPTION_UPDATED = 'subscription_updated'


class WebSocketMessage(BaseModel):
    type: WebSocketEvent
    data: dict[str, Any]
