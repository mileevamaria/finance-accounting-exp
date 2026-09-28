from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket_manager import manager

router = APIRouter(tags=['WebSocket'])


@router.websocket('/ws/companies/{company_id}')
async def company_socket(websocket: WebSocket, company_id: UUID):
    await manager.connect(company_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(
            company_id,
            websocket,
        )
