from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
from typing import Set

from ..core.database import get_db
from ..api.deps import get_current_user
from ..models.user import User

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, Set[WebSocket]] = {}

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        if user_id not in self.active:
            self.active[user_id] = set()
        self.active[user_id].add(ws)

    def disconnect(self, ws: WebSocket, user_id: str):
        if user_id in self.active:
            self.active[user_id].discard(ws)
            if not self.active[user_id]:
                del self.active[user_id]

    async def send_to_user(self, user_id: str, data: dict):
        if user_id in self.active:
            for ws in self.active[user_id]:
                try:
                    await ws.send_json(data)
                except Exception:
                    pass

    async def broadcast(self, data: dict):
        for user_sockets in self.active.values():
            for ws in user_sockets:
                try:
                    await ws.send_json(data)
                except Exception:
                    pass


manager = ConnectionManager()


@ws_router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, token: str):
    payload = decode_token(token)
    if not payload:
        await ws.close(code=4001)
        return
    user_id = payload["sub"]
    await manager.connect(ws, user_id)
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            await manager.send_to_user(user_id, {"echo": msg})
    except WebSocketDisconnect:
        manager.disconnect(ws, user_id)
    except Exception:
        manager.disconnect(ws, user_id)


from ..core.security import decode_token
