from typing import cast
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import WebSocket

from app.core.websocket_manager import ConnectionManager


@pytest.mark.asyncio
async def test_connect():
    manager = ConnectionManager()
    websocket_mock = AsyncMock()
    websocket = cast(WebSocket, websocket_mock)

    company_id = uuid4()
    await manager.connect(company_id, websocket)
    websocket_mock.accept.assert_awaited_once()

    assert company_id in manager.connections
    assert websocket in manager.connections[company_id]


@pytest.mark.asyncio
async def test_connect_multiple_websockets():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_1_mock = AsyncMock()
    websocket_2_mock = AsyncMock()

    websocket_1 = cast(WebSocket, websocket_1_mock)
    websocket_2 = cast(WebSocket, websocket_2_mock)

    await manager.connect(company_id, websocket_1)
    await manager.connect(company_id, websocket_2)

    websocket_1_mock.accept.assert_awaited_once()
    websocket_2_mock.accept.assert_awaited_once()

    assert manager.connections[company_id] == [
        websocket_1,
        websocket_2,
    ]


@pytest.mark.asyncio
async def test_disconnect():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_mock = AsyncMock()
    websocket = cast(WebSocket, websocket_mock)

    await manager.connect(company_id, websocket)

    manager.disconnect(company_id, websocket)

    assert company_id not in manager.connections


@pytest.mark.asyncio
async def test_disconnect_one_of_multiple_websockets():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_1_mock = AsyncMock()
    websocket_2_mock = AsyncMock()

    websocket_1 = cast(WebSocket, websocket_1_mock)
    websocket_2 = cast(WebSocket, websocket_2_mock)

    await manager.connect(company_id, websocket_1)
    await manager.connect(company_id, websocket_2)

    manager.disconnect(company_id, websocket_1)

    assert company_id in manager.connections
    assert manager.connections[company_id] == [websocket_2]


@pytest.mark.asyncio
async def test_disconnect_unknown_company():
    manager = ConnectionManager()

    company_id = uuid4()

    websocket_mock = AsyncMock()
    websocket = cast(WebSocket, websocket_mock)

    manager.disconnect(company_id, websocket)

    assert company_id not in manager.connections


@pytest.mark.asyncio
async def test_disconnect_unknown_websocket():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_1_mock = AsyncMock()
    websocket_2_mock = AsyncMock()

    websocket_1 = cast(WebSocket, websocket_1_mock)
    websocket_2 = cast(WebSocket, websocket_2_mock)

    await manager.connect(company_id, websocket_1)

    manager.disconnect(company_id, websocket_2)

    assert manager.connections[company_id] == [websocket_1]


@pytest.mark.asyncio
async def test_broadcast():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_1_mock = AsyncMock()
    websocket_2_mock = AsyncMock()

    websocket_1 = cast(WebSocket, websocket_1_mock)
    websocket_2 = cast(WebSocket, websocket_2_mock)

    await manager.connect(company_id, websocket_1)
    await manager.connect(company_id, websocket_2)

    message = {
        'type': 'account_updated',
        'data': {
            'account_id': str(uuid4()),
        },
    }

    await manager.broadcast(company_id, message)

    websocket_1_mock.send_json.assert_awaited_once_with(message)
    websocket_2_mock.send_json.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_broadcast_only_to_same_company():
    manager = ConnectionManager()

    company_1 = uuid4()
    company_2 = uuid4()

    websocket_1_mock = AsyncMock()
    websocket_2_mock = AsyncMock()

    websocket_1 = cast(WebSocket, websocket_1_mock)
    websocket_2 = cast(WebSocket, websocket_2_mock)

    await manager.connect(company_1, websocket_1)
    await manager.connect(company_2, websocket_2)

    message = {
        'type': 'account_updated',
        'data': {
            'account_id': str(uuid4()),
        },
    }

    await manager.broadcast(company_1, message)

    websocket_1_mock.send_json.assert_awaited_once_with(message)
    websocket_2_mock.send_json.assert_not_awaited()


@pytest.mark.asyncio
async def test_broadcast_to_unknown_company():
    manager = ConnectionManager()

    company_id = uuid4()

    message = {
        'type': 'account_updated',
        'data': {},
    }

    await manager.broadcast(company_id, message)

    assert company_id not in manager.connections


@pytest.mark.asyncio
async def test_broadcast_removes_disconnected_websocket():
    manager = ConnectionManager()
    company_id = uuid4()

    websocket_mock = AsyncMock()
    websocket = cast(WebSocket, websocket_mock)

    await manager.connect(company_id, websocket)

    websocket_mock.send_json.side_effect = RuntimeError(
        'connection is dead'
    )

    await manager.broadcast(
        company_id,
        {
            'type': 'account_updated',
            'data': {},
        },
    )

    assert company_id not in manager.connections
