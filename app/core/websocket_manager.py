from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[UUID, list[WebSocket]] = defaultdict(list)

    async def connect(self, company_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.connections[company_id].append(websocket)

    def disconnect(self, company_id: UUID, websocket: WebSocket):
        if company_id not in self.connections:
            return

        if websocket in self.connections[company_id]:
            self.connections[company_id].remove(websocket)

        if not self.connections[company_id]:
            del self.connections[company_id]

    async def broadcast(self, company_id: UUID, message: dict):
        if company_id not in self.connections:
            return

        disconnected = []

        for ws in self.connections[company_id]:
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append(ws)

        for ws in disconnected:
            self.disconnect(company_id, ws)


manager = ConnectionManager()
