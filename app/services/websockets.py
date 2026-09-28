from uuid import UUID

from app.core.websocket_manager import manager
from app.schemas.websockets import (
    WebSocketEvent,
    WebSocketMessage,
)


class WebSocketService:
    async def _broadcast(
        self,
        company_id: UUID,
        event: WebSocketEvent,
        data: dict,
    ) -> None:
        message = WebSocketMessage(type=event, data=data)
        await manager.broadcast(
            company_id,
            message.model_dump(mode='json'),
        )

    async def send_transaction_created(
        self,
        company_id: UUID,
        transaction_id: UUID,
        account_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.TRANSACTION_CREATED,
            {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        )

    async def send_transaction_updated(
        self,
        company_id: UUID,
        transaction_id: UUID,
        account_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.TRANSACTION_UPDATED,
            {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        )

    async def send_transaction_deleted(
        self,
        company_id: UUID,
        transaction_id: UUID,
        account_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.TRANSACTION_DELETED,
            {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        )

    async def send_account_updated(
        self,
        company_id: UUID,
        account_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.ACCOUNT_UPDATED,
            {
                'account_id': str(account_id),
            },
        )

    async def send_project_created(
        self,
        company_id: UUID,
        project_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.PROJECT_CREATED,
            {
                'project_id': str(project_id),
            },
        )

    async def send_project_updated(
        self,
        company_id: UUID,
        project_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.PROJECT_UPDATED,
            {
                'project_id': str(project_id),
            },
        )

    async def send_category_updated(
        self,
        company_id: UUID,
        category_id: UUID,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.CATEGORY_UPDATED,
            {
                'category_id': str(category_id),
            },
        )

    async def send_subscription_updated(
        self,
        company_id: UUID,
        plan: str,
        status: str,
    ) -> None:
        await self._broadcast(
            company_id,
            WebSocketEvent.SUBSCRIPTION_UPDATED,
            {
                'plan': plan,
                'status': status,
            },
        )
