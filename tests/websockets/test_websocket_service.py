from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.schemas.websockets import WebSocketEvent
from app.services.websockets import WebSocketService


@pytest.fixture
def websocket_service():
    return WebSocketService()


@pytest.mark.asyncio
async def test_send_transaction_created(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    transaction_id = uuid4()
    account_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_transaction_created(
        company_id,
        transaction_id,
        account_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.TRANSACTION_CREATED,
            'data': {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_transaction_updated(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    transaction_id = uuid4()
    account_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_transaction_updated(
        company_id,
        transaction_id,
        account_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.TRANSACTION_UPDATED,
            'data': {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_transaction_deleted(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    transaction_id = uuid4()
    account_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_transaction_deleted(
        company_id,
        transaction_id,
        account_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.TRANSACTION_DELETED,
            'data': {
                'transaction_id': str(transaction_id),
                'account_id': str(account_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_account_updated(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    account_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_account_updated(
        company_id,
        account_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.ACCOUNT_UPDATED,
            'data': {
                'account_id': str(account_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_project_created(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    project_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_project_created(
        company_id,
        project_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.PROJECT_CREATED,
            'data': {
                'project_id': str(project_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_project_updated(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    project_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_project_updated(
        company_id,
        project_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.PROJECT_UPDATED,
            'data': {
                'project_id': str(project_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_category_updated(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()
    category_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_category_updated(
        company_id,
        category_id,
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.CATEGORY_UPDATED,
            'data': {
                'category_id': str(category_id),
            },
        },
    )


@pytest.mark.asyncio
async def test_send_subscription_updated(
    websocket_service,
    monkeypatch,
):
    company_id = uuid4()

    broadcast_mock = AsyncMock()

    monkeypatch.setattr(
        'app.services.websockets.manager.broadcast',
        broadcast_mock,
    )

    await websocket_service.send_subscription_updated(
        company_id,
        'pro',
        'active',
    )

    broadcast_mock.assert_awaited_once_with(
        company_id,
        {
            'type': WebSocketEvent.SUBSCRIPTION_UPDATED,
            'data': {
                'plan': 'pro',
                'status': 'active',
            },
        },
    )
