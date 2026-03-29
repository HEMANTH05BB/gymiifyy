from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


class DatabaseClient:
    def __init__(self) -> None:
        self._memory: dict[str, list[dict[str, Any]]] = {"sessions": []}
        self._client: AsyncIOMotorClient | None = None
        self._db = None

        if settings.enable_db:
            self._client = AsyncIOMotorClient(settings.mongo_uri)
            self._db = self._client[settings.mongo_db_name]

    async def add_session(self, payload: dict[str, Any]) -> None:
        if self._db is not None:
            await self._db.sessions.insert_one(payload)
            return
        self._memory["sessions"].append(payload)

    async def get_sessions_by_user(self, user_id: str) -> list[dict[str, Any]]:
        if self._db is not None:
            cursor = self._db.sessions.find({"user_id": user_id}).sort("created_at", 1)
            return [doc async for doc in cursor]
        return [s for s in self._memory["sessions"] if s.get("user_id") == user_id]


database_client = DatabaseClient()
